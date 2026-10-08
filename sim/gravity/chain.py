"""Harmonic chain (lattice free scalar field, 1+1D) tools.

H = 1/2 sum pi_j^2 + 1/2 sum m^2 phi_j^2 + 1/2 sum_links (phi_{j+1}-phi_j)^2,
Dirichlet walls phi_0 = phi_{N+1} = 0 (sites 0..N-1 here).

Ground state: X = <phi phi> = V^{-1/2}/2, P = <pi pi> = V^{1/2}/2.
"""
import numpy as np


def potential(N, m, bump=None, link_bump=None):
    V = np.diag(np.full(N, 2.0 + m * m))
    V -= np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)
    if bump is not None:            # extra on-site stiffness  lambda*g_j*phi_j^2/2
        V += np.diag(bump)
    if link_bump is not None:       # extra link stiffness  lambda*g_l*(phi_{l+1}-phi_l)^2/2
        for l, w in enumerate(link_bump):
            if w:
                V[l, l] += w; V[l + 1, l + 1] += w
                V[l, l + 1] -= w; V[l + 1, l] -= w
    return V


def ground_corr(V):
    w, U = np.linalg.eigh(V)
    s = np.sqrt(w)
    X = 0.5 * (U / s) @ U.T
    P = 0.5 * (U * s) @ U.T
    return X, P


def symplectic_nu(XA, PA):
    # eigenvalues of sqrt(X P) via symmetric form X^1/2 P X^1/2
    w, U = np.linalg.eigh(XA)
    Xh = (U * np.sqrt(w)) @ U.T
    nu2 = np.linalg.eigvalsh(Xh @ PA @ Xh)
    return np.sqrt(np.clip(nu2, 0.25, None))


def entropy(XA, PA):
    nu = symplectic_nu(XA, PA)
    a, b = nu + 0.5, nu - 0.5
    with np.errstate(divide="ignore", invalid="ignore"):
        tb = np.where(b > 1e-300, b * np.log(b), 0.0)
    return float(np.sum(a * np.log(a) - tb))


def modular_matrices(XA, PA, eps_clip=60.0):
    """K = 1/2 (phi M phi + pi N pi) for the reduced Gaussian state."""
    w, U0 = np.linalg.eigh(XA)
    Xh = (U0 * np.sqrt(w)) @ U0.T
    Xmh = (U0 / np.sqrt(w)) @ U0.T
    nu2, U = np.linalg.eigh(Xh @ PA @ Xh)
    nu = np.sqrt(np.clip(nu2, 0.25 + 1e-15, None))
    E = np.log((nu + 0.5) / (nu - 0.5))
    E = np.minimum(E, eps_clip)
    M = Xmh @ U @ np.diag(nu * E) @ U.T @ Xmh
    N = Xh @ U @ np.diag(E / nu) @ U.T @ Xh
    return M, N


def local_energy(X, P, m, sites):
    """<h_j> per site: pi^2/2 + m^2 phi^2/2 + half of each adjacent link's gradient energy."""
    N = X.shape[0]
    d = np.diag(X)
    h = 0.5 * np.diag(P) + 0.5 * m * m * d
    # link energies (j, j+1), j = 0..N-2, plus wall links
    link = 0.5 * (d[1:] + d[:-1] - 2 * np.diag(X, 1))
    return h, link
