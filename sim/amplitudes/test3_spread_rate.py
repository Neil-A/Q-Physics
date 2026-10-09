"""SIM-SPEC-02 Test 3 — Spread rate = decoherence?

In §4 of the spec, fringe visibility between two histories is |f(dn)| with
f(dn) = integral of exp(i theta dn) d mu(theta), mu a positive measure over
clock rates. A sharp rate gives full visibility; a spread of rates lowers it.

Question: can the August dephasing results be read as exactly this — a
positive spread of clock rates whose width grows as coupling accumulates?

One family is used throughout: mu = the law of  omega = sum_k s_k g_k, with
independent signs s_k = +-1 (equal weight) and couplings g_k >= 0. Its width
is sigma = sqrt(sum_k g_k^2). Time plays the role of dn (t = 1, as in August).

  A. RESULTS-01 Test 1 sweep: visibility 1 - p, p in [0, 1].
     One coupling g(p) = arccos(1 - p) gives |E exp(i omega)| = |cos g| = 1 - p.
  B. RESULTS-01 Test 2a central spin: coherence prod_k |cos g_k|, g_k uniform
     in [0.5, 1.5], N = 1 .. 1000, 200 draws each. The same random draws are
     regenerated (same seed, same order as test2_chair.part_a).
     For N <= 16 the measure mu is enumerated atom by atom (2^N atoms) and its
     characteristic function is computed directly, independently of the
     product formula.

Pass (SIM-SPEC-02 §5 Test 3, fixed before the run): one family fits both,
with sigma growing monotonically as coupling accumulates. Read as: the
visibility from mu matches the August numbers to 1e-12; sigma rises with p
in A; sigma rises at every added spin in B; August's slope -0.81 of log
median coherence against N is reproduced. Consistency check only.
"""
import itertools
import json
import numpy as np

TOL = 1e-12


def visibility_enumerated(g, t=1.0):
    g = np.asarray(g, float)
    signs = np.array(list(itertools.product((-1.0, 1.0), repeat=len(g))))
    omega = signs @ g                       # every atom of mu, each with weight 2^-N
    return abs(np.mean(np.exp(1j * omega * t)))


def main():
    log = []
    say = lambda s: (print(s), log.append(s))

    # ---- A
    ps = np.linspace(0.0, 1.0, 201)
    gA = np.arccos(1 - ps)
    visA = np.array([visibility_enumerated([g]) for g in gA])
    errA = float(np.max(np.abs(visA - (1 - ps))))
    monoA = bool(np.all(np.diff(gA) > 0))
    say(f"A  Test 1 sweep: max |visibility from mu - (1-p)| = {errA:.2e};  sigma rises with p: {monoA}"
        f"  (sigma from {gA[0]:.3f} to {gA[-1]:.3f})")

    # ---- B  (regenerate August's draws exactly)
    RNG = np.random.default_rng(20260806)
    Ns = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    meds, enum_err, sig_meds = [], 0.0, []
    for N in Ns:
        vals, sigs = [], []
        for _ in range(200):
            g = RNG.uniform(0.5, 1.5, size=N)
            prod = abs(np.prod(np.cos(g)))
            if N <= 16:
                enum_err = max(enum_err, abs(visibility_enumerated(g) - prod))
            vals.append(prod)
            sigs.append(np.sqrt(np.sum(g ** 2)))
        meds.append(np.median(vals))
        sig_meds.append(np.median(sigs))
    meds = np.array(meds)
    m = meds > 1e-300
    slope = float(np.polyfit(Ns[m], np.log(meds[m]), 1)[0])
    say(f"B  central spin: enumeration vs product formula, N <= 16: max difference {enum_err:.2e}")
    say(f"   slope of log median coherence vs N: {slope:.4f}  (August: -0.8097)")

    # sigma along one accumulating environment: add spins one at a time
    rng2 = np.random.default_rng(7)
    g_all = rng2.uniform(0.5, 1.5, size=1000)
    sig_path = np.sqrt(np.cumsum(g_all ** 2))
    monoB = bool(np.all(np.diff(sig_path) > 0))
    p = np.polyfit(np.log(Ns), np.log(sig_meds), 1)[0]
    say(f"   sigma rises at every added spin (1000 spins): {monoB};  median sigma grows as N^{p:.3f}")

    passed = errA < TOL and enum_err < TOL and monoA and monoB and abs(slope + 0.8097) < 1e-3
    say(f"TEST 3: {'PASS' if passed else 'FAIL'}")
    with open("results/test3.json", "w") as f:
        json.dump(dict(A_max_err=errA, A_sigma_monotone=monoA, B_enum_max_err=enum_err,
                       B_slope=slope, B_sigma_monotone=monoB, B_sigma_growth_exponent=float(p),
                       passed=bool(passed)), f, indent=1)
    with open("results/test3_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
