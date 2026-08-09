"""Shared measures and helpers for SIM-SPEC-01.

Coherence measures follow Baumgratz-Cramer-Plenio 2014 (papers/).
All entropies in bits (log base 2) so that a qubit's maxima are 1 for both
the l1-norm and the relative entropy -- see the Test 1 warning about
comparing orderings rather than magnitudes.
"""

import numpy as np

TOL = 1e-12


def _eigvals(rho):
    w = np.linalg.eigvalsh(np.asarray(rho, dtype=complex))
    return np.clip(w.real, 0.0, None)


def vn_entropy(rho):
    """Von Neumann entropy in bits."""
    w = _eigvals(rho)
    w = w[w > TOL]
    return float(-np.sum(w * np.log2(w)))


def c_l1(rho):
    """l1-norm of coherence: sum of off-diagonal magnitudes."""
    r = np.asarray(rho, dtype=complex)
    return float(np.sum(np.abs(r)) - np.sum(np.abs(np.diag(r))))


def c_rel(rho):
    """Relative entropy of coherence: S(rho_diag) - S(rho), in bits."""
    r = np.asarray(rho, dtype=complex)
    d = np.diag(np.diag(r))
    return float(vn_entropy(d) - vn_entropy(r))


def c_l2_INVALID(rho):
    """Sum of squared off-diagonals.

    NOT a valid coherence monotone (BCP 2014). Present only so Test 1 can
    demonstrate the violation numerically. Never use as a measure.
    """
    r = np.asarray(rho, dtype=complex)
    off = np.abs(r) ** 2
    np.fill_diagonal(off, 0.0)
    return float(np.sum(off))


def c_geo_qubit(rho):
    """Geometric measure of coherence, qubit closed form."""
    r = np.asarray(rho, dtype=complex)
    x = abs(r[0, 1])
    return float(0.5 * (1.0 - np.sqrt(max(0.0, 1.0 - 4.0 * x * x))))


def bloch(rho):
    """Bloch vector of a qubit density matrix."""
    r = np.asarray(rho, dtype=complex)
    return np.array([
        2 * r[0, 1].real,
        -2 * r[0, 1].imag,
        (r[0, 0] - r[1, 1]).real,
    ])


def max_coherence_over_bases_qubit(rho):
    """Maximum l1 coherence of a qubit over every choice of reference basis.

    For a qubit the l1 coherence in the basis whose axis is n-hat equals
    |r_perp| = sqrt(|r|^2 - (r.n)^2), maximised at |r| by any n perpendicular
    to r. So the maximum is the Bloch vector length -- a basis-independent
    quantity. This is what makes the Test 2 'hand-picked basis' worry decidable.
    """
    return float(np.linalg.norm(bloch(rho)))


def purity(rho):
    r = np.asarray(rho, dtype=complex)
    return float(np.trace(r @ r).real)


def partial_trace_two(rho, dims, keep):
    """Partial trace of a bipartite density matrix."""
    dA, dB = dims
    r = np.asarray(rho, dtype=complex).reshape(dA, dB, dA, dB)
    if keep == 0:
        return np.einsum('ikjk->ij', r)
    return np.einsum('kikj->ij', r)


def lifetime_1e(t, y, level=None):
    """First crossing time of y below level (default y[0]/e), linearly interpolated.

    Returns np.nan if the curve never crosses inside the window.
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    if level is None:
        level = y[0] / np.e
    below = np.where(y <= level)[0]
    if below.size == 0:
        return float('nan')
    i = below[0]
    if i == 0:
        return float(t[0])
    y0, y1 = y[i - 1], y[i]
    if abs(y1 - y0) < TOL:
        return float(t[i])
    frac = (y0 - level) / (y0 - y1)
    return float(t[i - 1] + frac * (t[i] - t[i - 1]))


def fit_powerlaw(x, y):
    """Least-squares fit of log y = a + b log x. Returns (b, a, r2)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return float('nan'), float('nan'), float('nan')
    lx, ly = np.log(x[m]), np.log(y[m])
    b, a = np.polyfit(lx, ly, 1)
    pred = a + b * lx
    ss_res = np.sum((ly - pred) ** 2)
    ss_tot = np.sum((ly - ly.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > TOL else float('nan')
    return float(b), float(a), float(r2)


def spearman(a, b):
    """Spearman rank correlation without pulling in scipy.stats."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = np.sqrt(np.sum(ra ** 2) * np.sum(rb ** 2))
    return float(np.sum(ra * rb) / denom) if denom > TOL else float('nan')


def random_density(d, rank=None, rng=None):
    rng = rng or np.random.default_rng()
    rank = rank or d
    g = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    rho = g @ g.conj().T
    return rho / np.trace(rho).real


def is_diagonal(m, tol=1e-9):
    m = np.asarray(m, dtype=complex)
    off = m - np.diag(np.diag(m))
    return np.max(np.abs(off)) < tol
