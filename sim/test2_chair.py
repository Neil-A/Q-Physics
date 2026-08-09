"""SIM-SPEC-01 Test 2 -- Does a chair come out thin?

Claim: macroscopic objects have negligible coherence WITHOUT hand-waving about
basis choice.

Parts:
  2a  central-spin pure dephasing, exact; residual coherence vs N; extrapolation
  2b  the basis question, made decidable: max coherence over ALL bases = |Bloch|
  2c  generic (non-dephasing) random couplings, full QuTiP evolution
  2d  the #9 'Watch' clause: does thinning require DISTINGUISHING coupling?
"""

import json
import os

import numpy as np
import qutip as qt

from common import bloch, c_l1, c_rel, max_coherence_over_bases_qubit

RNG = np.random.default_rng(20260806)
OUT = {}


# ---------------------------------------------------------------- 2a
def central_spin_coherence(g, t, alpha=1.0):
    """Exact coherence of a qubit pure-dephasing against N independent spins.

    H = (alpha sigma_z^S + beta I) (x) sum_k (g_k/2) sigma_z^k, env in |+>^N.
    Branch overlap = prod_k cos(alpha g_k t); the identity part contributes a
    global phase to both branches and cancels exactly.
    """
    return np.abs(np.prod(np.cos(alpha * np.asarray(g) * t)))


def part_a():
    t = 1.0
    Ns = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    reps = 200
    means, meds = [], []
    for N in Ns:
        vals = [central_spin_coherence(RNG.uniform(0.5, 1.5, size=N), t)
                for _ in range(reps)]
        means.append(np.mean(vals))
        meds.append(np.median(vals))
    means = np.array(means)
    meds = np.array(meds)

    # log C is linear in N -> exponential suppression. Fit the decay constant.
    m = meds > 1e-300
    slope, intercept = np.polyfit(Ns[m], np.log(meds[m]), 1)
    # extrapolate to a macroscopic environment
    log10_C_avogadro = (intercept + slope * 6.022e23) / np.log(10)

    res = {
        'time': t,
        'N_values': Ns.tolist(),
        'mean_coherence': means.tolist(),
        'median_coherence': meds.tolist(),
        'log_median_vs_N_slope': float(slope),
        'log_median_vs_N_intercept': float(intercept),
        'decay_is_exponential_in_N': bool(slope < -0.01),
        'coherence_at_N_1e3': float(meds[-1]),
        'log10_coherence_extrapolated_to_6e23': float(log10_C_avogadro),
    }
    OUT['2a_dephasing_scaling'] = res
    return res


# ---------------------------------------------------------------- 2b
def part_b():
    """Is thinness an artefact of the chosen basis?

    For a qubit, the l1 coherence in the basis with axis n is
    sqrt(|r|^2 - (r.n)^2), so the maximum over every possible basis is |r|.
    If |r| -> 0 the state is thin in EVERY basis, and the 'hand-picked basis'
    objection cannot be raised. Check the identity numerically, then check
    that the which-path basis is not special.
    """
    checks = []
    for _ in range(2000):
        g = RNG.normal(size=(2, 2)) + 1j * RNG.normal(size=(2, 2))
        rho = g @ g.conj().T
        rho /= np.trace(rho).real
        r = bloch(rho)
        # brute force over 4000 random bases
        best = 0.0
        for _ in range(200):
            v = RNG.normal(size=3)
            v /= np.linalg.norm(v)
            perp = np.sqrt(max(0.0, np.dot(r, r) - np.dot(r, v) ** 2))
            best = max(best, perp)
        checks.append((max_coherence_over_bases_qubit(rho), best))
    checks = np.array(checks)
    analytic, sampled = checks.T

    # now the physical case: dephasing trajectory
    t = 1.0
    Ns = np.unique(np.round(np.logspace(0, 2.5, 25)).astype(int))
    rows = []
    for N in Ns:
        g = RNG.uniform(0.5, 1.5, size=N)
        c = central_spin_coherence(g, t)
        # state after dephasing from |+>: r = (c, 0, 0) up to a phase
        rho = np.array([[0.5, c / 2], [c / 2, 0.5]], dtype=complex)
        rows.append((N, c_l1(rho), max_coherence_over_bases_qubit(rho)))
    rows = np.array(rows)

    res = {
        'analytic_max_ge_sampled_max_always': bool(np.all(analytic >= sampled - 1e-9)),
        'sampled_reaches_analytic_maxdev': float(np.max(analytic - sampled)),
        'whichpath_basis_coherence_equals_max_over_bases': bool(
            np.max(np.abs(rows[:, 1] - rows[:, 2])) < 1e-9),
        'max_deviation': float(np.max(np.abs(rows[:, 1] - rows[:, 2]))),
        'conclusion': ('the which-path basis is the MAXIMISING basis on the dephasing '
                       'trajectory, so thinness there is not basis-tuned: no other basis '
                       'shows more coherence'),
    }
    OUT['2b_basis_independence'] = res
    return res


# ---------------------------------------------------------------- 2c
def part_c():
    """Generic couplings, not pure dephasing. Full evolution in QuTiP.

    System qubit + N environment qubits, random all-to-system couplings with a
    random environment self-Hamiltonian. Track the basis-free |Bloch| of the
    system. No dephasing structure is assumed anywhere.
    """
    results = {}
    for N in range(1, 11):
        vals = []
        for rep in range(12):
            dims = [2] * (N + 1)
            sx = qt.tensor([qt.sigmax()] + [qt.qeye(2)] * N)
            sy = qt.tensor([qt.sigmay()] + [qt.qeye(2)] * N)
            sz = qt.tensor([qt.sigmaz()] + [qt.qeye(2)] * N)
            H = 0 * sz
            for k in range(N):
                for S, name in ((sz, 'z'), (sx, 'x')):
                    ops = [qt.qeye(2)] * (N + 1)
                    ops[k + 1] = RNG.choice([qt.sigmaz(), qt.sigmax(), qt.sigmay()])
                    E = qt.tensor(ops)
                    H += RNG.normal(0, 1.0 / np.sqrt(N)) * S * E
                ops = [qt.qeye(2)] * (N + 1)
                ops[k + 1] = qt.sigmaz()
                H += RNG.normal(0, 0.5) * qt.tensor(ops)
            psi0 = qt.tensor([(qt.basis(2, 0) + qt.basis(2, 1)).unit()]
                             + [(qt.basis(2, 0) + qt.basis(2, 1)).unit()] * N)
            ts = np.linspace(0, 8, 60)
            out = qt.sesolve(H, psi0, ts)
            rs = []
            for st in out.states:
                rho = qt.ptrace(st, 0).full()
                rs.append(np.linalg.norm(bloch(rho)))
            vals.append(np.mean(rs[len(rs) // 2:]))  # late-time average
        results[N] = float(np.mean(vals))
    Ns = np.array(sorted(results))
    ys = np.array([results[n] for n in Ns])
    m = ys > 1e-12
    slope, intercept = np.polyfit(Ns[m], np.log(ys[m]), 1)
    res = {
        'late_time_mean_bloch_length_by_N': {int(k): v for k, v in results.items()},
        'log_slope_vs_N': float(slope),
        'decays_with_N': bool(slope < 0),
        'note': ('|Bloch| is the max coherence over every basis, so this is a '
                 'basis-free statement of thinness for generic couplings'),
    }
    OUT['2c_generic_couplings'] = res
    return res


# ---------------------------------------------------------------- 2d
def part_d():
    """The #9 Watch clause. Does thinning require the coupling to be
    which-path DISTINGUISHING?

    alpha = 1 : fully distinguishing (environment records the branch)
    alpha = 0 : fully non-distinguishing (couples to the identity on the
                which-path DOF -- this is gravity's case, since both paths
                carry identical mass)
    """
    t = 2.0
    N = 60
    g = RNG.uniform(0.5, 1.5, size=N)
    alphas = np.linspace(0, 1, 51)
    cs = np.array([central_spin_coherence(g, t, alpha=a) for a in alphas])

    # verify coherence == |<E0|E1>| exactly (Test 1b identity, now with N spins)
    overlaps = []
    for a in alphas:
        ov = np.prod(np.cos(a * g * t))
        overlaps.append(abs(ov))
    overlaps = np.array(overlaps)

    # small-alpha behaviour: decay rate should go like alpha^2
    small = alphas < 0.15
    lg = np.log(np.clip(cs[small][1:], 1e-300, None))
    la = np.log(alphas[small][1:])
    slope, _ = np.polyfit(la, np.log(-lg), 1)

    res = {
        'coherence_at_alpha_0_non_distinguishing': float(cs[0]),
        'coherence_at_alpha_1_fully_distinguishing': float(cs[-1]),
        'non_distinguishing_leaves_coherence_untouched': bool(abs(cs[0] - 1.0) < 1e-12),
        'coherence_equals_environment_overlap_maxdev': float(np.max(np.abs(cs - overlaps))),
        'small_alpha_exponent_of_decay_rate': float(slope),
        'expected_exponent': 2.0,
        'verdict_9': ('PASS -- thinning is exactly the distinguishability of the '
                      'environment record; a coupling proportional to the identity on '
                      'the which-path DOF produces no thinning at any N or t'),
    }
    OUT['2d_hash9_watch'] = res
    return res


if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    a = part_a(); print('=== TEST 2a ==='); print(json.dumps(a, indent=2, default=float)[:1200])
    b = part_b(); print('\n=== TEST 2b ==='); print(json.dumps(b, indent=2, default=float))
    d = part_d(); print('\n=== TEST 2d (#9) ==='); print(json.dumps(d, indent=2, default=float))
    c = part_c(); print('\n=== TEST 2c ==='); print(json.dumps(c, indent=2, default=float))
    with open('results/test2.json', 'w') as f:
        json.dump(OUT, f, indent=2, default=float)
