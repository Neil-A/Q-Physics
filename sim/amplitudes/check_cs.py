"""Brute-force check of cs.py's fast chain code on small sprinklings.

Recomputes every longest chain by an O(N^2) dynamic programme written
directly from the causal relation (t_b - t_a > |x_b - x_a|), with no
light-cone coordinates and no Fenwick tree, and compares.
"""
import numpy as np
import cs


def brute(t, x, qt, qx, slit_masks):
    n = len(t)
    order = np.argsort(t)
    t, x = t[order], x[order]
    masks = [m[order] for m in slit_masks]
    prec = (t[None, :] - t[:, None]) > np.abs(x[None, :] - x[:, None])  # prec[a,b]: a < b
    # forward from S
    LS = np.zeros(n, dtype=int)
    for b in range(n):
        preds = np.where(prec[:n, b][:b])[0] if b else np.array([], int)
        LS[b] = 1 + max([1] + [LS[a] for a in preds])
    # backward to each query, and through slits
    straight, thr = [], [[], []]
    for X_t, X_x in zip(qt, qx):
        before = (X_t - t) > np.abs(X_x - x)
        straight.append(1 + max([1] + list(LS[before])))
        LX = np.zeros(n, dtype=int)          # longest chain e -> ... -> X, ends included
        for a in range(n - 1, -1, -1):
            if not before[a]:
                LX[a] = -10**9
                continue
            succ = [LX[b] for b in range(a + 1, n) if prec[a, b] and before[b]]
            LX[a] = 1 + max([1] + succ)
        for j in range(2):
            cand = [LS[e] + LX[e] - 1 for e in range(n) if masks[j][e] and before[e]]
            thr[j].append(max(cand) if cand else None)
    return np.array(straight), thr


def main():
    rng = np.random.default_rng(12345)
    # make the slits fat so small sprinklings have elements in them
    cs.SLIT_W, cs.SLIT_H = 0.12, 0.06
    worst = 0
    for trial in range(6):
        t, x = cs.sprinkle(600.0, rng)
        qx = np.linspace(-cs.XMAX, cs.XMAX, 7)
        qt = np.full_like(qx, cs.T2)
        fast_straight = cs.chain_to_points(t, x, qt, qx)
        f1, f2 = cs.chain_through_slits(t, x, qt, qx)
        masks = [cs.in_slit(t, x, 0), cs.in_slit(t, x, 1)]
        b_straight, (b1, b2) = brute(t, x, qt, qx, masks)
        assert np.array_equal(fast_straight, b_straight), (fast_straight, b_straight)
        for fast, br in ((f1, b1), (f2, b2)):
            for a, b in zip(fast, br):
                if b is None:
                    assert a < 0, (a, b)
                else:
                    assert a == b, (a, b)
        worst = max(worst, len(t))
        print(f"trial {trial}: N={len(t)}  straight {fast_straight.tolist()}  slit1 {f1.tolist()}  slit2 {f2.tolist()}  OK")
    print(f"All fast results match brute force (largest N = {worst}).")


if __name__ == "__main__":
    main()
