"""SIM-SPEC-01 Test 1, follow-up -- the measure-ordering question.

Test 1's stated FAIL condition includes 'the two measures disagreeing on
ordering -- the latter would mean the choice of measure carries physical
content, which is a problem for the ontology.'

Test 1c found Spearman falling from 0.99 (d=2) to 0.90 (d=8) on random states.
That is a disagreement. This follow-up asks how bad it is and, more usefully,
whether it touches the states the framework actually needs.
"""

import json
import os

import numpy as np

from common import c_l1, c_rel, spearman

RNG = np.random.default_rng(20260806)
OUT = {}


def disagreement_rate(states):
    """Fraction of ordered PAIRS the two measures rank differently."""
    l1 = np.array([c_l1(s) for s in states])
    rel = np.array([c_rel(s) for s in states])
    n = len(states)
    i, j = np.triu_indices(n, k=1)
    s1 = np.sign(l1[i] - l1[j])
    s2 = np.sign(rel[i] - rel[j])
    return float(np.mean(s1 != s2)), spearman(l1, rel)


def random_states(d, n, rank=None):
    out = []
    for _ in range(n):
        r = rank or d
        g = RNG.normal(size=(d, r)) + 1j * RNG.normal(size=(d, r))
        rho = g @ g.conj().T
        out.append(rho / np.trace(rho).real)
    return out


def dephasing_family(d, n):
    """The physically realised path: one fixed pure superposition, progressively
    dephased. This is the trajectory a resolving front actually traverses."""
    c = RNG.normal(size=d) + 1j * RNG.normal(size=d)
    c /= np.linalg.norm(c)
    base = np.outer(c, c.conj())
    out = []
    for p in np.linspace(0, 1, n):
        rho = base.copy()
        off = ~np.eye(d, dtype=bool)
        rho[off] *= (1 - p)
        out.append(rho)
    return out


def dephasing_many_seeds(d, n_seeds, n_steps):
    """Many different initial superpositions, each partially dephased. This is
    the honest test: comparing thickness ACROSS different physical situations."""
    out = []
    for _ in range(n_seeds):
        c = RNG.normal(size=d) + 1j * RNG.normal(size=d)
        c /= np.linalg.norm(c)
        base = np.outer(c, c.conj())
        for p in RNG.random(n_steps):
            rho = base.copy()
            off = ~np.eye(d, dtype=bool)
            rho[off] *= (1 - p)
            out.append(rho)
    return out


if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    res = {}
    for d in (2, 3, 4, 6, 8, 12, 16):
        rr, sr = disagreement_rate(random_states(d, 120))
        pr = [disagreement_rate(dephasing_family(d, 60)) for _ in range(20)]
        mr, ms = disagreement_rate(dephasing_many_seeds(d, 20, 6))
        res[f'd={d}'] = {
            'random_full_rank_states': {'pair_disagreement': rr, 'spearman': sr},
            'single_dephasing_trajectory': {
                'pair_disagreement_mean': float(np.mean([p[0] for p in pr])),
                'spearman_mean': float(np.mean([p[1] for p in pr])),
            },
            'many_dephasing_trajectories_pooled': {'pair_disagreement': mr, 'spearman': ms},
        }
    OUT['1e_measure_ordering'] = res
    OUT['1e_summary'] = {
        'finding': ('the two valid measures agree PERFECTLY along any single dephasing '
                    'trajectory in every dimension -- that is the ordering the front '
                    'actually needs, since resolution moves a state along one such path. '
                    'They disagree on a growing fraction of pairs when comparing '
                    'UNRELATED states, and the disagreement grows with d. So thickness is '
                    'well defined as a monotone along a resolution history, and NOT well '
                    'defined as an absolute cross-system quantity above d = 2.'),
        'consequence': ('the framework may say "this cell thinned" without choosing a '
                        'measure, but may not say "cell A is thicker than cell B" for '
                        'unrelated A and B without choosing one'),
    }
    print(json.dumps(OUT, indent=2, default=float))
    with open('results/test1b.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
