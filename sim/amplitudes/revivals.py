"""Do a few partners resolve a particle, or only link with it? (10 Oct 2026)

Uses the August central-spin model (sim/test2_chair.py): a particle's
coherence against N partners with couplings g_k uniform in [0.5, 1.5] is
|prod_k cos(g_k t)|. With few partners the coherence keeps coming back (the
update goes out and returns: a link, not a record). With many it never does
within any reasonable time (the update has spread past the point of return).

Reports, over t in (5, 2000], the fraction of time coherence is above 0.5 and
the best return, averaged over 5 random draws per N. Supports the 10 Oct
"isolation" commitment in FRAMEWORK §15.
"""
import json
import numpy as np

rng = np.random.default_rng(20261010)
t = np.linspace(0, 2000, 2_000_001)
rows, log = [], []
for N in [1, 2, 3, 5, 10, 20]:
    fr, mx = [], []
    for _ in range(5):
        g = rng.uniform(0.5, 1.5, N)
        c = np.ones_like(t)
        for gk in g:
            c *= np.abs(np.cos(gk * t))
        late = c[t > 5]
        fr.append(float(np.mean(late > 0.5)))
        mx.append(float(late.max()))
    rows.append(dict(N=N, frac_above_half=float(np.mean(fr)), best_return=float(np.mean(mx))))
    line = f"N={N:2d}: time with coherence back above 0.5 = {np.mean(fr):.4f}; best return = {np.mean(mx):.3f}"
    print(line)
    log.append(line)
json.dump(rows, open("results/revivals.json", "w"), indent=1)
open("results/revivals_console.txt", "w").write("\n".join(log) + "\n")
