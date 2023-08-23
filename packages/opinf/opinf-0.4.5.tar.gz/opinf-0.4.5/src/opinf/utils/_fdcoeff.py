import numpy as np
import scipy.linalg as la


def _fd_coeff(dt, offset=0, order=4):
    """Get finite difference for a first derivative.

    Parameters
    ----------
    dt : float
        Time step (uniform spacing).
    offset : int
        Offset from the center of the stencil.
        - `offset = 0`: central difference scheme
        - `offset > 0`: forward difference scheme
        - `offset < 0`: backward difference scheme
    order : int
        Order of the finite difference scheme, i.e., order + 1 stencil points
        are used.

    Returns
    -------
    indices : (order + 1,) ndarray
        Indices of the stencil points.
    coeffs : (order + 1,) ndarray
        Coefficients of the finite difference stencil.
    """
    assert order % 2 == 0
    size = order + 1
    indices = np.arange(-size//2, size//2) + 1 + offset
    print("indices:", indices)
    d = np.zeros(size, dtype=int)
    d[1] = 1
    S = np.vander(indices, increasing=True).T
    return indices, np.round(la.solve(S, d) / (dt), 14)
