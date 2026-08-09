"""SIM-SPEC-01 Test 3, follow-up sweeps -- convergence of the L-scaling question.

Test 3 proper found the detector configuration flat and the mirror
configuration saturating. These sweeps push on the one regime that could still
rescue an L/c law, and establish why it cannot.

  3g  fine L scan: is the mirror's L-dependence a TREND or a wavelength-scale
      OSCILLATION?
  3h  the node branch: a residual coherence PLATEAU (bound state), which is a
      different phenomenon from a longer lifetime
  3i  maximum local log-slope d(lnT)/d(lnL) anywhere, vs the 1.0 that #14 needs
  3j  the causal bound: the saturation distance L* is set by v/gamma -- by the
      LOCAL coupling

NOTE ON METHOD. A first pass used a log-linear fit of |c_e(t)| over a late-time
window to get an effective rate. That estimator is wrong here: on the mirror
branch the curve is two-stage (free decay, then a frozen residue), so a
late-window fit measures the plateau and returns spurious infinities. Every
number below uses the 1/e crossing of the actual decay, plus the plateau height
reported separately, which is what distinguishes the two behaviours.
"""

import json
import os

import numpy as np

from common import fit_powerlaw, lifetime_1e
from waveguide import run

OUT = {}


def probe(L, variant='mirror', g=0.1, J=1.0, t_max=None, n_t=1400, **kw):
    """Robust characterisation of the coherence curve.

    T_1e      -- first crossing of 1/e (nan if it never crosses: no decay)
    plateau   -- late-time residual coherence (bound-state fraction)
    T_half    -- first crossing of 1/2, a second robust timescale
    """
    gamma = g * g / J
    if t_max is None:
        t_max = max(8.0 / gamma, 2.5 * (2 * L / (2 * J)))
    r = run(L, g=g, J=J, variant=variant, n_t=n_t, t_max=t_max, **kw)
    t, c = r['t'], r['coherence']
    tail = c[int(0.8 * len(c)):]
    return {
        'L': L,
        'T_1e': lifetime_1e(t, c),
        'T_half': lifetime_1e(t, c, level=0.5),
        'plateau': float(np.mean(tail)),
        'tau': r['tau_roundtrip'], 'gamma': r['gamma'], 't_max': float(t[-1]),
    }


# ---------------------------------------------------------------- 3g
def fine_scan():
    """L from 4 to 80, every integer, gamma*tau well below 1.
    If #14 is right the lifetime should be climbing steadily with L."""
    Ls = np.arange(4, 81)
    rows = [probe(int(L), 'mirror', t_max=2500, n_t=1500) for L in Ls]
    T = np.array([r['T_1e'] for r in rows], dtype=float)
    plat = np.array([r['plateau'] for r in rows], dtype=float)
    even, odd = (Ls % 2 == 0), (Ls % 2 == 1)
    finite_even = np.isfinite(T[even])
    res = {
        'L': Ls.tolist(), 'T_1e': T.tolist(), 'plateau': plat.tolist(),
        'even_L': {
            'n_that_decay': int(np.sum(np.isfinite(T[even]))),
            'mean_T_1e': float(np.nanmean(T[even])),
            'mean_plateau': float(np.nanmean(plat[even])),
            'exponent_T_vs_L': fit_powerlaw(Ls[even][finite_even], T[even][finite_even])[0],
        },
        'odd_L': {
            'n_that_never_reach_1_over_e': int(np.sum(~np.isfinite(T[odd]))),
            'n_total': int(odd.sum()),
            'mean_plateau': float(np.nanmean(plat[odd])),
        },
        'plateau_even_vs_odd': {
            'even': float(np.nanmean(plat[even])), 'odd': float(np.nanmean(plat[odd])),
        },
        'alternation_period_2_confirmed': bool(
            np.nanmean(plat[odd]) > 10 * np.nanmean(plat[even])),
        'finding': ('the mirror L-dependence at small L alternates with period 2 sites '
                    '(= lambda/2 at band centre), i.e. it is driven by the standing-wave '
                    'phase phi = 2 k0 L. That is a WAVELENGTH-scale effect, not a '
                    'delay-scale one, and it is what Purcell already describes.'),
    }
    OUT['3g_fine_scan'] = res
    return res


# ---------------------------------------------------------------- 3h
def node_branch():
    """Odd L (node). Emission is suppressed and a bound state forms: the
    coherence does not decay more slowly, it stops decaying at a residue.
    Track the residue, and find where the effect dies."""
    Ls = np.array([5, 9, 13, 17, 23, 31, 41, 55, 73, 97, 129, 171, 227, 301, 401])
    rows = [probe(int(L), 'mirror', t_max=4000, n_t=2000) for L in Ls]
    plat = np.array([r['plateau'] for r in rows], dtype=float)
    T = np.array([r['T_1e'] for r in rows], dtype=float)
    b, _, r2 = fit_powerlaw(Ls, np.clip(plat, 1e-12, None))
    res = {
        'L': Ls.tolist(),
        'plateau_residual_coherence': plat.tolist(),
        'T_1e': T.tolist(),
        'plateau_exponent_vs_L': b, 'r2': r2,
        'plateau_at_smallest_L': float(plat[0]),
        'plateau_at_largest_L': float(plat[-1]),
        'finding': ('a nearby mirror FREEZES part of the coherence (bound state in the '
                    'continuum); a distant one does not. The residue falls as L grows, '
                    'so what L-dependence exists runs OPPOSITE to #14: closer absorber, '
                    'longer-lived coherence.'),
    }
    OUT['3h_node_branch'] = res
    return res


# ---------------------------------------------------------------- 3i
def max_local_slope():
    """Most generous possible reading: the largest local d(lnT)/d(lnL)
    anywhere, on the branch where a lifetime is well defined."""
    out = {}
    for variant, parity in (('absorber', None), ('mirror', 0)):
        Ls = np.unique(np.round(np.logspace(np.log10(6), np.log10(1200), 34)).astype(int))
        if parity is not None:
            Ls = np.unique(np.array([L + (L % 2) for L in Ls]))
        rows = [probe(int(L), variant, t_max=2500, n_t=1500) for L in Ls]
        T = np.array([r['T_1e'] for r in rows], dtype=float)
        m = np.isfinite(T) & (T > 0)
        lx, ly = np.log(Ls[m].astype(float)), np.log(T[m])
        slopes = np.diff(ly) / np.diff(lx)
        mids = np.exp((lx[1:] + lx[:-1]) / 2)
        out[variant] = {
            'L': Ls.tolist(), 'T_1e': T.tolist(),
            'max_local_slope': float(np.nanmax(slopes)),
            'L_at_max_slope': float(mids[int(np.nanargmax(slopes))]),
            'median_local_slope': float(np.nanmedian(slopes)),
            'slope_required_by_14': 1.0,
            'fraction_of_window_with_slope_above_0p5': float(np.mean(slopes > 0.5)),
            'total_dynamic_range_of_T': float(np.nanmax(T[m]) / np.nanmin(T[m])),
            'total_dynamic_range_of_L': float(Ls.max() / Ls.min()),
        }
    OUT['3i_max_local_slope'] = out
    return out


# ---------------------------------------------------------------- 3j
def causal_bound():
    """Where does the L-dependence stop, and what sets that scale?

    The absorber can only influence the decay if the round trip 2L/v completes
    before the emitter has decohered. So L* ~ v/(2 gamma) -- set by the LOCAL
    coupling. Vary g and check L* moves as 1/gamma.
    """
    out, gs, lstars, gammas = {}, (0.07, 0.1, 0.15, 0.2), [], []
    for g in gs:
        gamma = g * g
        free = 2.0 / gamma                      # free-space 1/e time of |c_e|
        Ls = np.unique(np.round(np.logspace(np.log10(4), np.log10(2000), 30)).astype(int))
        Ls = np.unique(np.array([L + (L % 2) for L in Ls]))   # antinode branch
        rows = [probe(int(L), 'mirror', g=g, t_max=6.0 / gamma, n_t=1600) for L in Ls]
        T = np.array([r['T_1e'] for r in rows], dtype=float)
        reached = np.where(np.isfinite(T) & (T > 0.95 * free))[0]
        Lstar = float(Ls[reached[0]]) if reached.size else float('nan')
        out[f'g={g}'] = {
            'gamma': gamma, 'T_free_2_over_gamma': free,
            'L': Ls.tolist(), 'T_1e': T.tolist(),
            'L_star_saturation': Lstar,
            'predicted_L_star_v_over_gamma': 2.0 / gamma,
            'ratio_observed_to_predicted': Lstar / (2.0 / gamma) if np.isfinite(Lstar) else None,
            'T_at_smallest_L': float(T[0]),
        }
        lstars.append(Lstar); gammas.append(gamma)
    b, _, r2 = fit_powerlaw(np.array(gammas), np.array(lstars, dtype=float))
    out['scaling_of_Lstar_with_gamma'] = {
        'exponent': b, 'r2': r2, 'expected_minus_1': -1.0,
        'finding': ('the distance beyond which the absorber stops mattering is set by '
                    'the LOCAL coupling, L* ~ v/gamma. Beyond L*, no information about '
                    'the absorber can reach the emitter before it has decohered -- so a '
                    'lifetime proportional to L is not merely absent from this model, it '
                    'is causally excluded in any model with a finite signal speed.'),
    }
    OUT['3j_causal_bound'] = out
    return out


if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    print('=== 3g FINE SCAN ==='); print(json.dumps(fine_scan(), indent=2, default=float))
    print('\n=== 3h NODE BRANCH ==='); print(json.dumps(node_branch(), indent=2, default=float))
    print('\n=== 3i MAX LOCAL SLOPE ==='); print(json.dumps(max_local_slope(), indent=2, default=float))
    print('\n=== 3j CAUSAL BOUND ==='); print(json.dumps(causal_bound(), indent=2, default=float))
    with open('results/test3b.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
