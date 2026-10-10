# sim/amplitudes — SIM-SPEC-02

Code for [SIM-SPEC-02](../../SIM-SPEC-02-amplitudes.md); results in [RESULTS-03](../../RESULTS-03-amplitudes.md).
Needs NumPy, SciPy, Numba, Matplotlib (no QuTiP).

| File | What it does |
|---|---|
| `cs.py` | Causal-set core: Poisson sprinkling in 1+1, longest chains (light-cone coordinates + Fenwick tree), continuum proper times |
| `check_cs.py` | Recomputes every chain by brute force from the causal relation and compares |
| `test1_link_clock.py` | Test 1: link counts as clocks for the double slit |
| `test1b_followup.py` | Follow-up on Test 1's spacing bias (written after the verdict) |
| `test2_positivity.py` | Test 2: positivity alone and under composition |
| `test3_spread_rate.py` | Test 3: decoherence as a spread of clock rates |
| `make_figures.py` | Figures from the committed JSON |
| `revivals.py` | August central-spin model: how often coherence comes back with few vs many partners (10 Oct, supports the isolation commitment) |

Things to know before changing anything:
1. Chain lengths count elements, both ends included. Calibration and test use the same convention, so it cancels.
2. A slit must hold elements. At ρ = 10⁴ a 0.02 × 0.02 slit is sometimes empty; Test 1 starts at 3 × 10⁴.
3. The clock is calibrated on straight histories and used on bent ones. Calibrating on the test histories themselves would absorb the geometry and make Test 1 trivial.
4. Test 2's kernels and its search use separate random streams. Sharing one stream made the kernel set depend on the search.
