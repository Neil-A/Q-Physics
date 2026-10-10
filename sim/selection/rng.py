"""A random stream for each seed, for use inside numba loops.

Each seed has its own 64-bit state (splitmix64). The result does not depend
on how the threads share the work, so a run is exactly reproducible. Two runs
that start from the same states get the same random kicks, step for step.
"""
import math

import numba as nb
import numpy as np

_G = np.uint64(0x9E3779B97F4A7C15)
_M1 = np.uint64(0xBF58476D1CE4E5B9)
_M2 = np.uint64(0x94D049BB133111EB)
_S30 = np.uint64(30)
_S27 = np.uint64(27)
_S31 = np.uint64(31)
_S11 = np.uint64(11)
_TWO53 = 1.0 / 9007199254740992.0


@nb.njit
def next_u01(state):
    """Return (new state, uniform number in (0, 1))."""
    state = state + _G
    z = state
    z = (z ^ (z >> _S30)) * _M1
    z = (z ^ (z >> _S27)) * _M2
    z = z ^ (z >> _S31)
    return state, ((z >> _S11) + 0.5) * _TWO53


@nb.njit
def normal_pair(state):
    """Return (new state, n1, n2): two independent standard normal numbers."""
    state, u1 = next_u01(state)
    state, u2 = next_u01(state)
    r = math.sqrt(-2.0 * math.log(u1))
    return state, r * math.cos(2 * math.pi * u2), r * math.sin(2 * math.pi * u2)


def states(n, seed):
    """Start states for n seeds, from a fixed integer seed list."""
    return np.random.default_rng(seed).integers(1, 2 ** 63, size=n, dtype=np.int64).astype(np.uint64)
