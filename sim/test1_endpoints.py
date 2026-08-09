"""SIM-SPEC-01 Test 1 -- Endpoint behaviour.

Claim: coherence is high for a live superposition, zero for a resolved outcome.

Parts:
  1a  qubit dephasing sweep, three valid measures, monotonicity + endpoints
  1b  entanglement entropy runs the OTHER way (the inversion argument)
  1c  d > 2: maxima differ, orderings still agree
  1d  the l2 (squared off-diagonal) measure is not a monotone -- found by search
"""

import json
import numpy as np

from common import (c_geo_qubit, c_l1, c_l2_INVALID, c_rel, partial_trace_two,
                    spearman, vn_entropy)

RNG = np.random.default_rng(20260806)
OUT = {}


# ---------------------------------------------------------------- 1a
def part_a():
    ps = np.linspace(0.0, 1.0, 201)
    rows = []
    for p in ps:
        c = (1 - p) / 2
        rho = np.array([[0.5, c], [c, 0.5]], dtype=complex)
        rows.append((p, c_l1(rho), c_rel(rho), c_geo_qubit(rho)))
    arr = np.array(rows)
    p, l1, rel, geo = arr.T

    def monotone(y):
        return bool(np.all(np.diff(y) <= 1e-12))

    res = {
        'endpoints': {
            'l1_super': l1[0], 'l1_dephased': l1[-1],
            'rel_super': rel[0], 'rel_dephased': rel[-1],
            'geo_super': geo[0], 'geo_dephased': geo[-1],
        },
        'monotone': {'l1': monotone(l1), 'rel': monotone(rel), 'geo': monotone(geo)},
        'ordering_agreement_spearman': {
            'l1_vs_rel': spearman(l1, rel),
            'l1_vs_geo': spearman(l1, geo),
            'rel_vs_geo': spearman(rel, geo),
        },
        'max_abs_gap_l1_minus_rel': float(np.max(np.abs(l1 - rel))),
    }
    OUT['1a_qubit_sweep'] = res
    np.save('results/test1_sweep.npy', arr)
    return res


# ---------------------------------------------------------------- 1b
def part_b():
    """System qubit + environment qubit, partial which-path record.

    |psi(th)> = (|0>|E0> + |1>|E1(th)>)/sqrt2 with <E0|E1> = cos(th).
    Global state is pure, so S(rho_S) IS the entanglement entropy.
    """
    ths = np.linspace(0.0, np.pi / 2, 201)
    rows = []
    for th in ths:
        e0 = np.array([1.0, 0.0], dtype=complex)
        e1 = np.array([np.cos(th), np.sin(th)], dtype=complex)
        psi = (np.kron([1, 0], e0) + np.kron([0, 1], e1)) / np.sqrt(2)
        rho = np.outer(psi, psi.conj())
        rs = partial_trace_two(rho, (2, 2), keep=0)
        rows.append((th, c_l1(rs), c_rel(rs), vn_entropy(rs), abs(np.vdot(e0, e1))))
    arr = np.array(rows)
    th, l1, rel, ent, ov = arr.T

    res = {
        'coherence_at_no_record': {'l1': l1[0], 'rel': rel[0]},
        'coherence_at_full_record': {'l1': l1[-1], 'rel': rel[-1]},
        'entanglement_entropy_at_no_record': ent[0],
        'entanglement_entropy_at_full_record': ent[-1],
        'spearman_l1_vs_entropy': spearman(l1, ent),
        'coherence_equals_env_overlap_maxdev': float(np.max(np.abs(l1 - ov))),
    }
    OUT['1b_inversion'] = res
    np.save('results/test1_inversion.npy', arr)
    return res


# ---------------------------------------------------------------- 1c
def part_c():
    out = {}
    for d in (2, 3, 4, 6, 8):
        maxc = np.ones(d, dtype=complex) / np.sqrt(d)
        rho_max = np.outer(maxc, maxc.conj())
        # random states, ranked by each measure
        l1s, rels = [], []
        for _ in range(400):
            g = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
            rho = g @ g.conj().T
            rho /= np.trace(rho).real
            l1s.append(c_l1(rho))
            rels.append(c_rel(rho))
        out[f'd={d}'] = {
            'max_l1_theory_d_minus_1': d - 1,
            'max_l1_observed_on_max_coherent_state': c_l1(rho_max),
            'max_rel_theory_log2_d': float(np.log2(d)),
            'max_rel_observed_on_max_coherent_state': c_rel(rho_max),
            'spearman_l1_vs_rel_random_states': spearman(l1s, rels),
        }
    OUT['1c_dimension_scaling'] = out
    return out


# ---------------------------------------------------------------- 1d
def _random_incoherent_kraus(d, n_ops, rng):
    """Incoherent operations: each Kraus operator has at most one nonzero
    entry per column, so it maps every incoherent state to an incoherent state.
    Normalised to sum_i K_i^dag K_i = I."""
    maps = [rng.integers(0, d, size=d) for _ in range(n_ops)]
    amps = rng.random((n_ops, d))
    amps /= np.sqrt(np.sum(amps ** 2, axis=0, keepdims=True))
    phases = np.exp(2j * np.pi * rng.random((n_ops, d)))
    ks = []
    for a in range(n_ops):
        K = np.zeros((d, d), dtype=complex)
        for col in range(d):
            K[maps[a][col], col] = amps[a, col] * phases[a, col]
        ks.append(K)
    return ks


def part_d():
    """Search for an incoherent operation that INCREASES the squared-off-diagonal
    quantity -- reproducing BCP's counterexample numerically."""
    best = None
    for d in (2, 3, 4):
        for _ in range(200000):
            ks = _random_incoherent_kraus(d, RNG.integers(2, 4), RNG)
            g = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
            rho = g @ g.conj().T
            rho /= np.trace(rho).real
            out = sum(K @ rho @ K.conj().T for K in ks)
            before, after = c_l2_INVALID(rho), c_l2_INVALID(out)
            # sanity: the valid measures must not increase
            gain = after - before
            if gain > 1e-6:
                valid_ok = (c_l1(out) <= c_l1(rho) + 1e-9) and (c_rel(out) <= c_rel(rho) + 1e-9)
                if best is None or gain > best['increase']:
                    best = {'d': int(d), 'l2_before': before, 'l2_after': after,
                            'increase': gain,
                            'l1_before': c_l1(rho), 'l1_after': c_l1(out),
                            'rel_before': c_rel(rho), 'rel_after': c_rel(out),
                            'valid_measures_still_monotone': bool(valid_ok)}
            if best is not None and best['increase'] > 0.05:
                break
        if best is not None and best['increase'] > 0.05:
            break
    OUT['1d_l2_not_a_monotone'] = best or {'found': False}
    return best


if __name__ == '__main__':
    import os
    os.makedirs('results', exist_ok=True)
    a = part_a(); b = part_b(); c = part_c(); d = part_d()

    print('=== TEST 1a: qubit dephasing sweep ===')
    print(json.dumps(a, indent=2, default=float))
    print('\n=== TEST 1b: inversion (coherence down, entanglement entropy up) ===')
    print(json.dumps(b, indent=2, default=float))
    print('\n=== TEST 1c: dimension scaling ===')
    print(json.dumps(c, indent=2, default=float))
    print('\n=== TEST 1d: l2 is not a monotone ===')
    print(json.dumps(d, indent=2, default=float))

    with open('results/test1.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
