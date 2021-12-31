import numpy as np
from numba import jit, prange
from numba import NumbaDeprecationWarning, NumbaPendingDeprecationWarning, NumbaWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaWarning)


@jit("float64[:](int8, int8)",parallel=True)
def Levy(n, T):
    y = np.zeros(n)
    D = np.random.exponential(2 * T)
    d = int(D)
    for i in prange(n):
        y[i] =np.tan(np.random.uniform(0, np.pi, d)).sum()
    return y-0.5
