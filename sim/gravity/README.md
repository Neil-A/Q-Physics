# sim/gravity/ — the area-law route to gravity

Lattice checks and tests for the gravity-origin route reopened on 7 October 2026. Results and interpretation in [RESULTS-02-gravity.md](../../RESULTS-02-gravity.md).

Plain NumPy/SciPy; no QuTiP needed. Uses the same pinned `../requirements.txt`. Re-run 8 Oct 2026 on Python 3.13.16 (NumPy 2.5.3, SciPy 1.18.1) and reproduced the recorded numbers.

## Run

```bash
cd sim/gravity
python first_law.py && python rindler_scan.py && python ball3d_squeeze.py && python ball3d_fit.py && python tests_2_4.py
```

About a minute in total. Everything writes JSON to `results/`.

## Files

| File | What it does |
|---|---|
| `chain.py` | Harmonic-chain (lattice free scalar) tools: ground-state correlations, entanglement entropy, the exact modular Hamiltonian of a region |
| `first_law.py` | 1D: does a region's entanglement change by 2π × distance-weighted energy change? Sanity check against the exact modular operator, and the small-interval ("ball") sweep |
| `rindler_scan.py` | 1D horizon (half-line) case across three masses and two kinds of nudge. **The canonical horizon result.** |
| `ball3d.py` | Radial (partial-wave) chain for 3+1D. Its own `__main__` run, a mass-term bump, was **discarded**: in 3+1D that changes the field's short-distance structure and the energy response grows with the cutoff |
| `ball3d_squeeze.py` | 3+1D small ball: squeeze one smooth spherical wave (UV-safe), compare entanglement change with plain and improved energy |
| `ball3d_fit.py` | 54 configurations: fits which correction the 3D lattice needs, then the ratio with theory's coefficients (improved energy density + Wald surface term) |
| `tests_2_4.py` | Test 2 (clock slowing vs distance from Earth, GR vs a local-load rule; GPS) and test 4 (light bending at the Sun, time-only vs full) by ray tracing |

## Things to know before changing anything

**Disturbances must be small.** A site (mass) bump must stay well below m² (the scan uses 1% of m²); `first_law.py rindler` used bumps larger than m² for the lightest mass and is kept only as the superseded first run.

**Massless 1D chains: use stiffness (gradient) bumps, not mass bumps.** In 1+1D the field φ itself is dominated by its longest-wavelength modes, so a φ² bump on a massless chain tests the infrared, not the 2π rule.

**Far from the horizon both numbers go to zero.** Beyond about 1.5 correlation lengths the true entanglement change is exponentially small and the lattice's version of energy density dominates the comparison. Read ratios there as lattice error, not physics.

**In 3+1D, a squeezed mode wholly inside the ball changes nothing.** Entanglement can't change under a unitary acting only inside the region; the real test needs the wave to straddle the edge.
