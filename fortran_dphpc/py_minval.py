"""
Reduction examples using the python frontend of DaCe.

python -m fortran_dphpc.py_minval
"""

import numpy as np

import dace
from dace.transformation.interstate import GPUTransformSDFG

N = dace.symbol("N")

@dace.program
def minval_py(A: dace.float64[N], R: dace.float64[1]):
    R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)


print("Creating SDFG...")
sdfg = minval_py.to_sdfg()
sdfg.apply_transformations(GPUTransformSDFG)
sdfg.simplify()
sdfg.compile()
