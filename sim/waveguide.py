"""Waveguide model for SIM-SPEC-01 Test 3 -- the L-sweep.

Design requirement 1 (model class): 1D tight-binding waveguide, finite
bandwidth, emitter coupled at one site. This is standard waveguide QED; the
absorber/mirror at distance L is an actual object in the model, not a rate.

Design requirement 2 (how L enters): L is the NUMBER OF LATTICE SITES between
the emitter and the terminator. It appears nowhere else -- not in the coupling
g, not in any decay rate, not in the bath spectral density. Nothing in the
model says 'a transaction completes when a signal returns from L'. Any
L-dependence in the output is produced by propagation alone.

Dispersion: omega(k) = -2J cos k, band [-2J, 2J].
Emitter is resonant with the band centre, k0 = pi/2, group velocity v = 2J.
Markovian (wide-band) spontaneous emission rate: gamma = 2 g^2 / v = g^2 / J.

Single-excitation sector, so the state is a vector
    [c_e, c_0, c_1, ..., c_{M-1}]
and the emitter coherence of the superposition (|g,vac> + |e,vac>)/sqrt2 is
    C(t) = |c_e(t)|
because only the amplitude still ON the emitter overlaps the un-emitted branch;
once the photon is in the field, that branch is orthogonal in the field sector.
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import expm_multiply


def build_atom(L, g=0.1, g2=0.3, kappa_a=0.15, J=1.0, left_pad=400,
               cap_len=300, cap_strength=0.6):
    """Emitter + waveguide + a REAL absorbing atom at distance L.

    Basis: [c_emitter, c_absorber, field sites 0..M-1].
    The absorber atom is itself damped at rate kappa_a into its own reservoir,
    which is what makes its record irreversible. L is still only the number of
    lattice sites between the two atoms.
    """
    n_e = left_pad
    n_L = n_e + L
    M = n_L + cap_len
    dim = M + 2
    rows, cols, vals = [], [], []

    rows += [0, 2 + n_e]; cols += [2 + n_e, 0]; vals += [g, g]        # emitter
    rows += [1, 2 + n_L]; cols += [2 + n_L, 1]; vals += [g2, g2]      # absorber
    rows += [1]; cols += [1]; vals += [-1j * kappa_a]                 # record sink

    for n in range(M - 1):
        rows += [2 + n, 2 + n + 1]; cols += [2 + n + 1, 2 + n]; vals += [-J, -J]

    for i in range(min(cap_len, n_e)):
        s = cap_strength * ((cap_len - i) / cap_len) ** 2
        rows.append(2 + i); cols.append(2 + i); vals.append(-1j * s)
    for i in range(cap_len):
        n = n_L + i
        if n >= M:
            break
        s = cap_strength * (i / cap_len) ** 2
        rows.append(2 + n); cols.append(2 + n); vals.append(-1j * s)

    H = sp.coo_matrix((vals, (rows, cols)), shape=(dim, dim), dtype=complex).tocsr()
    return H, n_e, n_L, M


def build(L, g=0.1, J=1.0, left_pad=None, cap_len=300, cap_strength=0.6,
          variant='absorber', barrier=0.0):
    """Return (H_eff sparse, n_e, n_L, M).

    variant:
      'absorber' -- complex absorbing potential ramp starting at n_L (a
                    detector that swallows the photon: record forms, no echo)
      'mirror'   -- chain terminates at n_L (perfect reflection: the confirmation
                    comes back, delayed feedback with round trip tau = 2L/v)
      'partial'  -- real barrier of height `barrier` at n_L, CAP beyond it
    """
    if left_pad is None:
        left_pad = 400
    n_e = left_pad                      # emitter couples here
    n_L = n_e + L                       # terminator sits here

    if variant == 'mirror':
        M = n_L + 1                     # hard wall: chain simply stops
    else:
        M = n_L + cap_len

    dim = M + 1                         # emitter + M field sites
    rows, cols, vals = [], [], []

    # emitter-field coupling
    rows += [0, 1 + n_e]
    cols += [1 + n_e, 0]
    vals += [g, g]

    # nearest-neighbour hopping
    for n in range(M - 1):
        rows += [1 + n, 1 + n + 1]
        cols += [1 + n + 1, 1 + n]
        vals += [-J, -J]

    # left-hand complex absorbing potential: the open channel
    for i in range(min(cap_len, n_e)):
        n = i
        s = cap_strength * ((cap_len - i) / cap_len) ** 2
        rows.append(1 + n); cols.append(1 + n); vals.append(-1j * s)

    if variant == 'absorber':
        for i in range(cap_len):
            n = n_L + i
            if n >= M:
                break
            s = cap_strength * (i / cap_len) ** 2
            rows.append(1 + n); cols.append(1 + n); vals.append(-1j * s)
    elif variant == 'partial':
        rows.append(1 + n_L); cols.append(1 + n_L); vals.append(barrier)
        for i in range(1, cap_len):
            n = n_L + i
            if n >= M:
                break
            s = cap_strength * (i / cap_len) ** 2
            rows.append(1 + n); cols.append(1 + n); vals.append(-1j * s)

    H = sp.coo_matrix((vals, (rows, cols)), shape=(dim, dim), dtype=complex).tocsr()
    return H, n_e, n_L, M


def evolve(H, dim, t_max, n_t):
    """|psi(t)> for psi(0) = emitter excited. Returns (times, amplitudes)."""
    psi0 = np.zeros(dim, dtype=complex)
    psi0[0] = 1.0
    A = (-1j) * H
    out = expm_multiply(A, psi0, start=0.0, stop=t_max, num=n_t, endpoint=True)
    ts = np.linspace(0.0, t_max, n_t)
    return ts, out


def run(L, g=0.1, J=1.0, t_max=None, n_t=600, variant='absorber',
        cap_len=300, left_pad=None, barrier=0.0):
    """Emitter coherence C(t) = |c_e(t)| plus the arrival signal at the terminator."""
    gamma = g * g / J
    v = 2.0 * J
    tau = 2.0 * L / v
    if t_max is None:
        # long enough to see the 1/e crossing (near 2/gamma) and, when the
        # round trip is short enough to matter, several feedback intervals
        t_max = max(8.0 / gamma, min(1.5 * tau + 4.0 / gamma, 40.0 / gamma))
    if left_pad is None:
        # the leftward photon only has to reach the absorbing ramp; it never
        # needs to traverse v*t_max. Convergence in this is checked explicitly.
        left_pad = 400
    if variant == 'atom':
        H, n_e, n_L, M = build_atom(L, g=g, J=J, cap_len=cap_len, left_pad=left_pad,
                                    **({'g2': barrier} if barrier else {}))
        off = 2
    else:
        H, n_e, n_L, M = build(L, g=g, J=J, variant=variant, cap_len=cap_len,
                               left_pad=left_pad, barrier=barrier)
        off = 1
    ts, psi = evolve(H, H.shape[0], t_max, n_t)
    c_e = psi[:, 0]
    coherence = np.abs(c_e)
    site_at_L = np.abs(psi[:, off + n_L]) ** 2 if n_L < M else np.zeros_like(ts)
    norm = np.sum(np.abs(psi) ** 2, axis=1)
    return {
        'L': L, 'g': g, 'J': J, 'gamma': gamma, 'v': v,
        'tau_roundtrip': 2 * L / v,
        't': ts, 'coherence': coherence,
        'excitation_at_terminator': site_at_L,
        'norm': norm,
        'n_e': n_e, 'n_L': n_L, 'M': M,
    }
