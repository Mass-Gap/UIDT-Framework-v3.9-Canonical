# Research Scripts

Experimental and exploratory verification scripts for UIDT framework development.

## Purpose

This directory contains research-grade scripts that explore:
- Novel verification approaches
- Experimental parameter studies
- Exploratory numerical methods
- Prototype implementations

## Status

Scripts in this directory are:
- **NOT production-ready**
- **NOT part of the canonical verification pipeline**
- **Subject to frequent changes**
- **May contain incomplete or experimental code**

## Production Pipeline

For canonical verification scripts, see:
- `verification/scripts/` (root level) - Production verification
- `verification/tests/` - Automated test suite

## Usage

Research scripts are intended for:
1. Exploring new verification methods
2. Prototyping numerical techniques
3. Investigating parameter sensitivities
4. Developing future production scripts

## Migration Path

When a research script matures:
1. Code review and cleanup
2. Add comprehensive documentation
3. Add error handling and validation
4. Move to `verification/scripts/` (production)
5. Add to automated test suite if applicable

## Evidence Category

Results from research scripts are:
- **Category [E]** by default (exploratory)
- Require independent verification before upgrade
- Must be validated against production pipeline

## Contributing

When adding research scripts:
- Use descriptive filenames
- Include docstring explaining purpose
- Document any non-standard dependencies
- Mark experimental sections clearly
- Add TODO comments for known issues

---

**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**DOI:** 10.5281/zenodo.17835200
