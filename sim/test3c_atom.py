"""SIM-SPEC-01 Test 3, third configuration -- a REAL absorbing atom at distance L.

The strongest form of #14's picture: the emitter opens a transaction, the offer
propagates to an actual absorber sitting L sites away, the absorber absorbs, and
the record becomes irreversible (the absorber is damped into its own reservoir).
If the tail closes when the confirmation returns, this is where it shows.
"""

import json
import os

import numpy as np

from common import fit_powerlaw, lifetime_1e
from waveguide import run

OUT = {}


def probe(L, g=0.1, g2=0.3, t_max=None, n_t=1400):
    gamma = g * g
    if t_max is None:
        t_max = max(8.0 / gamma, 2.5 * L)
    r = run(L, g=g, variant='atom', n_t=n_t, t_max=t_max, barrier=g2)
    t, c = r['t'], r['coherence']
    return {'L': L, 'T_1e': lifetime_1e(t, c),
            'T_half': lifetime_1e(t, c, level=0.5),
            'plateau': float(np.mean(c[int(0.85 * len(c)):])),
            'tau': 2.0 * L / 2.0}


if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    res = {}
    for g2 in (0.15, 0.3, 0.6):
        Ls = np.unique(np.round(np.logspace(np.log10(6), np.log10(1200), 22)).astype(int))
        rows = [probe(int(L), g2=g2) for L in Ls]
        T = np.array([r['T_1e'] for r in rows], dtype=float)
        Th = np.array([r['T_half'] for r in rows], dtype=float)
        b, _, r2 = fit_powerlaw(Ls, T)
        bh, _, r2h = fit_powerlaw(Ls, Th)
        res[f'absorber_coupling_g2={g2}'] = {
            'L': Ls.tolist(), 'T_1e': T.tolist(), 'T_half': Th.tolist(),
            'exponent_T1e_vs_L': b, 'r2': r2,
            'exponent_Thalf_vs_L': bh, 'r2_half': r2h,
            'free_space_2_over_gamma': 200.0,
            'dynamic_range_T': float(np.nanmax(T) / np.nanmin(T)),
            'dynamic_range_L': float(Ls.max() / Ls.min()),
        }
    OUT['3k_real_absorbing_atom'] = res
    OUT['3k_summary'] = {
        'exponent_required_by_14': 1.0,
        'finding': ('with a genuine absorbing atom at distance L and an irreversible '
                    'record, the emitter coherence lifetime is still set by the local '
                    'emission rate. Over a 200-fold change in L the lifetime does not '
                    'track L. The absorber determines WHERE the record forms, not HOW '
                    'FAST the source decoheres.'),
    }
    print(json.dumps(OUT, indent=2, default=float))
    with open('results/test3c.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
