#!/usr/bin/env python3
"""
UIDT v3.6.1 — SHA-256 Checksum Generator
=========================================

Generates cryptographic checksums for all files in the Clay submission package.
Ensures immutability and integrity verification for reviewers.

Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

Usage:
    python checksums_sha256_gen.py [--output SHA256_MANIFEST.txt] [--verify]
"""

import os
import sys
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

# Directories to hash
HASH_DIRECTORIES = [
    '00_CoverLetter',
    '01_Manuscript',
    '02_VerificationCode',
    '03_AuditData',
    '04_Certificates',
    '05_LatticeSimulation',
    '06_Figures',
    '07_MonteCarlo',
    '08_Documentation',
    '09_Supplementary_JSON',
    '10_VerificationReports'
]

# Files in root to hash
ROOT_FILES = [
    'README.md',
    'Dockerfile.clay_audit',
    'requirements.txt'
]

# Extensions to include
INCLUDE_EXTENSIONS = {
    '.py', '.tex', '.md', '.txt', '.csv', '.json', '.cff', 
    '.yaml', '.yml', '.bib', '.bbl', '.pdf', '.png'
}

# Files to exclude
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.git',
    '.pyc',
    'SHA256_MANIFEST'
]


# ============================================================================
# HASH FUNCTIONS
# ============================================================================

def compute_sha256(filepath: Path) -> str:
    """
    Compute SHA-256 hash of a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Hexadecimal SHA-256 hash string
    """
    sha256_hash = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        # Read in chunks for large files
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()


def compute_sha384(filepath: Path) -> str:
    """Compute SHA-384 hash."""
    sha384_hash = hashlib.sha384()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha384_hash.update(chunk)
    return sha384_hash.hexdigest()


def compute_sha512(filepath: Path) -> str:
    """Compute SHA-512 hash."""
    sha512_hash = hashlib.sha512()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha512_hash.update(chunk)
    return sha512_hash.hexdigest()


# ============================================================================
# FILE DISCOVERY
# ============================================================================

def should_include_file(filepath: Path) -> bool:
    """
    Determine if a file should be included in the manifest.
    
    Args:
        filepath: Path to check
        
    Returns:
        True if file should be hashed
    """
    # Check exclusion patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(filepath):
            return False
    
    # Check extension
    if filepath.suffix.lower() in INCLUDE_EXTENSIONS:
        return True
    
    # Include files without extension if they look like text
    if filepath.suffix == '':
        return filepath.name in ['Dockerfile', 'Makefile', 'LICENSE']
    
    return False


def discover_files(base_path: Path) -> List[Path]:
    """
    Discover all files to hash.
    
    Args:
        base_path: Root directory of the package
        
    Returns:
        List of file paths
    """
    files = []
    
    # Hash directories
    for dir_name in HASH_DIRECTORIES:
        dir_path = base_path / dir_name
        if dir_path.exists():
            for filepath in dir_path.rglob('*'):
                if filepath.is_file() and should_include_file(filepath):
                    files.append(filepath)
    
    # Hash root files
    for filename in ROOT_FILES:
        filepath = base_path / filename
        if filepath.exists():
            files.append(filepath)
    
    # Sort for deterministic output
    files.sort()
    
    return files


# ============================================================================
# MANIFEST GENERATION
# ============================================================================

def generate_manifest(base_path: Path) -> Dict[str, str]:
    """
    Generate SHA-256 manifest for all files.
    
    Args:
        base_path: Root directory
        
    Returns:
        Dictionary mapping relative paths to hashes
    """
    manifest = {}
    files = discover_files(base_path)
    
    print(f"Hashing {len(files)} files...")
    
    for filepath in files:
        rel_path = filepath.relative_to(base_path)
        hash_value = compute_sha256(filepath)
        manifest[str(rel_path)] = hash_value
        print(f"  {rel_path}: {hash_value[:16]}...")
    
    return manifest


def write_manifest(manifest: Dict[str, str], 
                   output_path: Path,
                   base_path: Path) -> None:
    """
    Write manifest to file.
    
    Args:
        manifest: Hash dictionary
        output_path: Output file path
        base_path: Base directory for metadata
    """
    timestamp = datetime.now().isoformat()
    
    with open(output_path, 'w') as f:
        f.write("=" * 78 + "\n")
        f.write("UIDT v3.6.1 — SHA-256 CRYPTOGRAPHIC MANIFEST\n")
        f.write("=" * 78 + "\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Files: {len(manifest)}\n")
        f.write(f"Algorithm: SHA-256\n")
        f.write("=" * 78 + "\n\n")
        
        # Group by directory
        current_dir = None
        for filepath, hash_value in sorted(manifest.items()):
            file_dir = str(Path(filepath).parent)
            
            if file_dir != current_dir:
                current_dir = file_dir
                f.write(f"\n[{current_dir}]\n")
                f.write("-" * 70 + "\n")
            
            f.write(f"{hash_value}  {filepath}\n")
        
        f.write("\n" + "=" * 78 + "\n")
        f.write("VERIFICATION INSTRUCTIONS\n")
        f.write("=" * 78 + "\n")
        f.write("""
To verify integrity on Linux/Mac:
    sha256sum -c SHA256_MANIFEST.txt

To verify on Windows (PowerShell):
    Get-FileHash -Algorithm SHA256 <filepath>

Any modification to any file will produce a different hash.
This manifest guarantees the immutability of the submission.
""")
        
        # Compute manifest hash
        manifest_content = "".join(f"{h}{p}" for p, h in sorted(manifest.items()))
        manifest_hash = hashlib.sha256(manifest_content.encode()).hexdigest()
        
        f.write("\n" + "=" * 78 + "\n")
        f.write("MANIFEST INTEGRITY\n")
        f.write("=" * 78 + "\n")
        f.write(f"Manifest SHA-256: {manifest_hash}\n")
        f.write("=" * 78 + "\n")
    
    print(f"\nManifest written to: {output_path}")
    print(f"Manifest hash: {manifest_hash}")


# ============================================================================
# VERIFICATION
# ============================================================================

def verify_manifest(manifest_path: Path, base_path: Path) -> Tuple[int, int, List[str]]:
    """
    Verify files against manifest.
    
    Args:
        manifest_path: Path to manifest file
        base_path: Base directory
        
    Returns:
        (passed, failed, error_list)
    """
    passed = 0
    failed = 0
    errors = []
    
    print("Verifying file integrity...")
    
    hash_line_re = re.compile(r'^(?P<hash>[0-9a-f]{64})\s{2}(?P<path>.+)$')

    with open(manifest_path, 'r') as f:
        for line in f:
            line = line.strip()

            m = hash_line_re.match(line)
            if not m:
                continue

            expected_hash = m.group('hash')
            rel_path = Path(m.group('path'))
            filepath = base_path / rel_path
            if filepath.exists():
                actual_hash = compute_sha256(filepath)
                if actual_hash == expected_hash:
                    passed += 1
                    print(f"  ✓ {rel_path}")
                else:
                    failed += 1
                    errors.append(f"{rel_path}: HASH MISMATCH")
                    print(f"  ✗ {rel_path} - HASH MISMATCH")
            else:
                failed += 1
                errors.append(f"{rel_path}: FILE NOT FOUND")
                print(f"  ✗ {rel_path} - FILE NOT FOUND")
    
    return passed, failed, errors


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='UIDT v3.6.1 SHA-256 Checksum Generator'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='04_Certificates/SHA256_MANIFEST.txt',
        help='Output manifest path'
    )
    parser.add_argument(
        '--verify', '-v',
        action='store_true',
        help='Verify existing manifest'
    )
    parser.add_argument(
        '--base', '-b',
        type=str,
        default='.',
        help='Base directory path'
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.base).resolve()
    output_path = base_path / args.output
    
    print("=" * 70)
    print("UIDT v3.6.1 — SHA-256 CHECKSUM GENERATOR")
    print("=" * 70)
    print(f"Base directory: {base_path}")
    print()
    
    if args.verify:
        # Verification mode
        if not output_path.exists():
            print(f"ERROR: Manifest not found: {output_path}")
            return 1
        
        passed, failed, errors = verify_manifest(output_path, base_path)
        
        print()
        print("=" * 70)
        print("VERIFICATION RESULT")
        print("=" * 70)
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"  - {error}")
            return 1
        else:
            print("\n✅ ALL FILES VERIFIED")
            return 0
    
    else:
        # Generation mode
        manifest = generate_manifest(base_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_manifest(manifest, output_path, base_path)
        
        print()
        print("=" * 70)
        print("MANIFEST GENERATION COMPLETE")
        print("=" * 70)
        print(f"Total files hashed: {len(manifest)}")
        print(f"Output: {output_path}")
        print()
        print("✅ Cryptographic integrity established")
        
        return 0


if __name__ == '__main__':
    sys.exit(main())
