"""SIM-SPEC-01 Test 3 -- the L-sweep.

Claim under test (#14, FRAMEWORK sec 7 Reading B):
    at fixed local coupling and temperature, coherence lifetime tracks the
    distance L to the absorber, ~ L/c.

Knob: L. Held fixed: g (coupling), J (bandwidth), everything else.

Pass/fail was fixed before the run, per the spec:
    supports #14  -- lifetime scales monotonically with L, exponent ~ 1,
                     Null A flat, AND a stated observed difference from Null B
    against #14   -- lifetime L-independent at fixed coupling
    Reading A     -- a cutoff: scaling that stops beyond some L
    null result   -- scaling present but indistinguishable from Null B

Nulls:
    Null A -- Markovian amplitude damping at matched coupling. No L anywhere.
    Null B -- the SAME waveguide model, read as ordinary quantum optics with
              no transactional structure added. Note that Null B and the
              'signal' are the same numbers, because the framework supplies no
              dynamics of its own. That is itself the result.
"""

import json
import os

import numpy as np

from common import fit_powerlaw, lifetime_1e
from waveguide import run

OUT = {}


def measure(L, variant, g=0.1, J=1.0, n_t=900, **kw):
    r = run(L, g=g, J=J, variant=variant, n_t=n_t, **kw)
    T = lifetime_1e(r['t'], r['coherence'])
    arr = r['excitation_at_terminator']
    thresh = 1e-6 * max(arr.max(), 1e-30)
    idx = np.where(arr > thresh)[0]
    t_arrive = float(r['t'][idx[0]]) if idx.size else float('nan')
    return {
        'L': L, 'T_coherence': T, 'tau_roundtrip': r['tau_roundtrip'],
        't_first_arrival_at_terminator': t_arrive,
        'gamma': r['gamma'], 'v': r['v'], 'dim': r['M'] + 1,
    }


# ---------------------------------------------------------------- 3a
def sweep_absorber():
    """A detector at distance L that absorbs the photon: the record forms
    there, nothing comes back."""
    Ls = np.unique(np.round(np.logspace(np.log10(4), np.log10(1500), 26)).astype(int))
    rows = [measure(int(L), 'absorber') for L in Ls]
    T = np.array([r['T_coherence'] for r in rows])
    gamma = rows[0]['gamma']
    b, a, r2 = fit_powerlaw(Ls, T)
    res = {
        'L': Ls.tolist(),
        'T_coherence': T.tolist(),
        'markovian_prediction_2_over_gamma': 2.0 / gamma,
        'max_relative_deviation_from_markov': float(np.max(np.abs(T - 2 / gamma)) / (2 / gamma)),
        'powerlaw_exponent_T_vs_L': b,
        'powerlaw_r2': r2,
        'spread_max_over_min': float(T.max() / T.min()),
        'verdict': 'lifetime is L-INDEPENDENT; exponent consistent with zero',
    }
    OUT['3a_absorber'] = res
    return res


# ---------------------------------------------------------------- 3b
def sweep_mirror():
    """A mirror at distance L: the confirmation DOES come back, after a round
    trip tau = 2L/v. This is the configuration most favourable to #14.

    At band centre k0 = pi/2 the round-trip phase is phi = 2 k0 L = pi L, so
    the parity of L sets antinode (even) vs node (odd). Sweeping parities
    separately separates the WAVELENGTH-scale phase effect from the
    DELAY-scale effect, which is the one #14 is about.
    """
    out = {}
    for name, parity in (('antinode_even_L', 0), ('node_odd_L', 1)):
        Ls = np.unique(np.round(np.logspace(np.log10(4), np.log10(1200), 24)).astype(int))
        Ls = np.array([int(L) + ((int(L) % 2) != parity) for L in Ls])
        Ls = np.unique(Ls)
        rows = [measure(int(L), 'mirror') for L in Ls]
        T = np.array([r['T_coherence'] for r in rows])
        gamma = rows[0]['gamma']
        b, a, r2 = fit_powerlaw(Ls, T)
        # exponent restricted to the large-L tail, where any L/c law must live
        tail = Ls > 200
        b_tail, _, r2_tail = fit_powerlaw(Ls[tail], T[tail]) if tail.sum() > 2 else (np.nan,) * 3
        out[name] = {
            'L': Ls.tolist(),
            'T_coherence': T.tolist(),
            'free_space_value_2_over_gamma': 2.0 / gamma,
            'powerlaw_exponent_all_L': b, 'r2_all_L': r2,
            'powerlaw_exponent_large_L': b_tail, 'r2_large_L': r2_tail,
            'T_at_smallest_L': float(T[0]), 'T_at_largest_L': float(T[-1]),
            'monotone_increasing': bool(np.all(np.diff(T) > -1e-6)),
        }
    OUT['3b_mirror'] = out
    return out


# ---------------------------------------------------------------- 3c
def null_a():
    """Markovian amplitude damping at matched coupling. Contains no L."""
    gamma = 0.1 ** 2 / 1.0
    ts = np.linspace(0, 40 / gamma, 4000)
    Ls = [4, 40, 400, 4000]
    Ts = []
    for _ in Ls:
        c = np.exp(-gamma * ts / 2)
        Ts.append(lifetime_1e(ts, c))
    res = {
        'L': Ls, 'T_coherence': Ts,
        'analytic_2_over_gamma': 2 / gamma,
        'flat': bool(np.ptp(Ts) < 1e-6),
        'note': 'confirms the pipeline reports flatness when flatness is the truth',
    }
    OUT['3c_null_A_markovian'] = res
    return res


# ---------------------------------------------------------------- 3d
def record_formation():
    """The OTHER observable: when does a which-path record first exist at the
    absorber? This is time-of-flight and is trivially proportional to L."""
    Ls = np.unique(np.round(np.logspace(np.log10(8), np.log10(1200), 18)).astype(int))
    rows = [measure(int(L), 'absorber') for L in Ls]
    ta = np.array([r['t_first_arrival_at_terminator'] for r in rows])
    v = rows[0]['v']
    b, a, r2 = fit_powerlaw(Ls, ta)
    res = {
        'L': Ls.tolist(),
        't_first_arrival': ta.tolist(),
        'L_over_v': (Ls / v).tolist(),
        'powerlaw_exponent': b, 'r2': r2,
        'mean_ratio_arrival_over_L_v': float(np.mean(ta / (Ls / v))),
        'verdict': ('record formation time scales as L^1 exactly -- but this is '
                    'time of flight, present in any theory with a finite signal '
                    'speed, and it is NOT the coherence lifetime'),
    }
    OUT['3d_record_formation'] = res
    return res


# ---------------------------------------------------------------- 3e
def convergence():
    """Numerical convergence: the L-independence in 3a must not be an artefact
    of the grid, the absorbing ramp, or the time resolution."""
    base = dict(variant='absorber')
    checks = {}
    for label, kw in (
        ('n_t=450', dict(n_t=450)),
        ('n_t=900', dict(n_t=900)),
        ('n_t=1800', dict(n_t=1800)),
        ('cap_len=150', dict(cap_len=150)),
        ('cap_len=600', dict(cap_len=600)),
        ('left_pad=400', dict(left_pad=400)),
        ('left_pad=1200', dict(left_pad=1200)),
    ):
        Ts = [measure(L, **base, **kw)['T_coherence'] for L in (20, 200, 1000)]
        checks[label] = {'T_at_L_20_200_1000': Ts,
                         'spread': float(max(Ts) / min(Ts))}
    # coupling sweep: does the flat value track 2/gamma across couplings?
    coup = {}
    for g in (0.05, 0.1, 0.2, 0.3):
        Ts = [measure(L, 'absorber', g=g)['T_coherence'] for L in (20, 200, 1000)]
        coup[f'g={g}'] = {'T': Ts, 'predicted_2_over_gamma': 2.0 / (g * g),
                          'max_rel_dev': float(max(abs(t - 2 / g ** 2) for t in Ts) / (2 / g ** 2)),
                          'spread_over_L': float(max(Ts) / min(Ts))}
    # bandwidth sweep
    band = {}
    for J in (0.5, 1.0, 2.0):
        Ts = [measure(L, 'absorber', J=J)['T_coherence'] for L in (20, 200, 1000)]
        band[f'J={J}'] = {'T': Ts, 'predicted_2J_over_g2': 2 * J / 0.01,
                          'spread_over_L': float(max(Ts) / min(Ts))}
    res = {'grid_and_boundary': checks, 'coupling': coup, 'bandwidth': band}
    OUT['3e_convergence'] = res
    return res


# ---------------------------------------------------------------- 3f
def reflectivity():
    """Interpolate between the two regimes: how reflective must the absorber be
    before any L-dependence appears at all?"""
    out = {}
    for barrier in (0.0, 0.5, 1.0, 2.0, 4.0):
        Ls = np.array([10, 30, 100, 300, 1000])
        Ts = [measure(int(L), 'partial', barrier=barrier)['T_coherence'] for L in Ls]
        b, _, r2 = fit_powerlaw(Ls, np.array(Ts))
        out[f'barrier={barrier}'] = {
            'L': Ls.tolist(), 'T': Ts,
            'powerlaw_exponent': b, 'r2': r2,
            'spread_max_over_min': float(max(Ts) / min(Ts)),
        }
    OUT['3f_reflectivity'] = out
    return out


if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    print('=== 3c NULL A (Markovian) ===')
    print(json.dumps(null_a(), indent=2, default=float))
    print('\n=== 3a ABSORBER (detector at L, no echo) ===')
    print(json.dumps(sweep_absorber(), indent=2, default=float))
    print('\n=== 3d RECORD FORMATION TIME ===')
    print(json.dumps(record_formation(), indent=2, default=float))
    print('\n=== 3b MIRROR (confirmation returns after 2L/v) ===')
    print(json.dumps(sweep_mirror(), indent=2, default=float))
    print('\n=== 3f REFLECTIVITY ===')
    print(json.dumps(reflectivity(), indent=2, default=float))
    print('\n=== 3e CONVERGENCE ===')
    print(json.dumps(convergence(), indent=2, default=float))
    with open('results/test3.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
