"""3+1D small-ball check with a UV-safe disturbance.

A mass bump changes the field's short-distance structure in 3+1D (its energy
response grows with the cutoff), so instead squeeze ONE smooth, spherically
symmetric mode of the massless scalar field. Only the l = 0 partial wave
changes, and the modular Hamiltonian splits by angular momentum, so the l = 0
radial chain carries the whole test.

Mode: Q = sum u_j phi_j, Pm = sum u_j pi_j (u normalised). Squeeze by lambda:
  phi -> (I + (e^lam - 1) u u^T) phi,   pi -> (I + (e^-lam - 1) u u^T) pi.

Compared, at first order (symmetric difference in lambda):
  dS            change in the ball's entanglement entropy
  dK_canonical  2*pi-weighted canonical energy change, beta = 2*pi (R^2-r^2)/(2R)
  dK_improved   same with T00 - (1/6) Laplacian(phi^2)  (conformal coupling)
"""
import json
import numpy as np
from chain import ground_corr, entropy
from ball3d import radial_V

XI = 1.0 / 6.0


def run(n, Nfac=8, x0f=0.45, wf=0.15, lam=1e-3):
    N = Nfac * n
    j = np.arange(1, N + 1, dtype=float)
    R = n + 0.5
    beta = lambda r: np.pi * (R * R - r * r) / R
    X0, P0 = ground_corr(radial_V(N, 0, 0.0))
    x0, w = x0f * R, max(wf * R, 1.0)
    u = np.exp(-((j - x0) ** 2) / (2 * w * w)); u /= np.linalg.norm(u)
    uu = np.outer(u, u)
    vals = {}
    for s in (1, -1):
        A = np.eye(N) + (np.exp(s * lam) - 1) * uu
        B = np.eye(N) + (np.exp(-s * lam) - 1) * uu
        X = A @ X0 @ A.T; P = B @ P0 @ B.T
        S = entropy(X[:n, :n], P[:n, :n])
        d = np.diag(X); off = np.diag(X, 1)
        site_e = 0.5 * np.diag(P)                       # l = 0, massless: no on-site potential
        jj, jn = j[:-1], j[1:]
        link_e = 0.5 * (jj + 0.5) ** 2 * (d[:-1] / jj ** 2 + d[1:] / jn ** 2 - 2 * off / (jj * jn))
        Kcan = np.sum(beta(j[:n]) * site_e[:n]) + np.sum(beta(j[:n - 1] + 0.5) * link_e[:n - 1])
        phi2 = d / (4 * np.pi * j ** 2)                 # <phi(x)^2> from the l=0 wave
        vals[s] = (S, Kcan, phi2)
    dS = (vals[1][0] - vals[-1][0]) / 2
    dK = (vals[1][1] - vals[-1][1]) / 2
    f = (vals[1][2] - vals[-1][2]) / 2
    lap = np.zeros(N)
    for k in range(N):
        jk = j[k]; fp = f[k + 1] if k + 1 < N else 0.0; fm = f[k - 1] if k > 0 else f[k]
        lap[k] = ((jk + 0.5) ** 2 * (fp - f[k]) - (jk - 0.5) ** 2 * (f[k] - fm)) / jk ** 2
    vol = 4 * np.pi * j ** 2
    dK_imp = dK - XI * np.sum(beta(j[:n]) * lap[:n] * vol[:n])
    return {"n": n, "R": R, "N": N, "mode_center": x0, "mode_width": w,
            "dS": dS, "dK_canonical": dK, "dK_improved": dK_imp,
            "ratio_canonical": dS / dK, "ratio_improved": dS / dK_imp}


if __name__ == "__main__":
    out = []
    for n in (8, 16, 32, 64, 128):
        r = run(n); out.append(r)
        print("R=%6.1f dS=%+.4e  ratio canonical=%.4f  ratio improved=%.4f" % (r["R"], r["dS"], r["ratio_canonical"], r["ratio_improved"]), flush=True)
    print("position scan, R=64.5")
    for x0f in (0.2, 0.45, 0.7):
        r = run(64, x0f=x0f); out.append(r)
        print("  center=%.2fR ratio canonical=%.4f improved=%.4f" % (x0f, r["ratio_canonical"], r["ratio_improved"]), flush=True)
    json.dump(out, open("results/ball3d_squeeze.json", "w"), indent=1)
