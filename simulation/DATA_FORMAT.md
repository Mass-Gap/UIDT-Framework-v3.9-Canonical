# UIDT Lattice Data Format Specification

**ILDG-Compatible Lattice QCD Data Format**

## Lattice Configurations

### Grid Specifications
- **Lattice Size:** 32³ × 64 (spatial × temporal)
- **Lattice Spacing:** a = 0.08 fm
- **Physical Volume:** (2.56 fm)³ × 5.12 fm
- **Gauge Group:** SU(3)

### Ensemble Parameters
- **β:** 6.0 (inverse bare coupling)
- **κ:** 0.500 ± 0.008
- **λ_S:** 5κ²/3 ≈ 0.41̄6̄ ± 0.007
- **Configurations:** 1000 (thermalized)
- **Separation:** 10 trajectories

### File Format (ILDG-Compatible)
```
gauge_config_XXXX.dat
```
Where XXXX = configuration number (0000-0999)

**Binary Structure:**
- Header: 512 bytes (metadata)
- Data: 4 × 32³ × 64 × 3 × 3 complex128 (gauge links)

## Measurement Observables

### Wilson Loops
- **Sizes:** 1×1 to 8×8
- **Format:** CSV with columns: R, T, ⟨W(R,T)⟩, σ_stat

### Spectral Gap
- **Observable:** Lowest non-zero eigenvalue of Dirac operator
- **Format:** JSON with fields: config_id, eigenvalue, residual

### String Tension
- **Observable:** σ from linear fit to V(R)
- **Format:** JSON with fields: σ, χ²/dof, fit_range

## ILDG Metadata

```xml
<?xml version="1.0"?>
<ildgFormat xmlns="http://www.lqcd.org/ildg">
  <version>1.0</version>
  <precision>64</precision>
  <lx>32</lx>
  <ly>32</ly>
  <lz>32</lz>
  <lt>64</lt>
  <datatype>4D_SU3_GAUGE_3x3</datatype>
</ildgFormat>
```

---
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)
