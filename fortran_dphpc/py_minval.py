"""
Reduction examples using the python frontend of DaCe.

python -m fortran_dphpc.reduce
"""

import os
import numpy as np

import dace

from dace.transformation.dataflow import GPUTransformMap
from dace.transformation.interstate import GPUTransformSDFG

N = dace.symbol("N")

@dace.program
def simple_reduction(A: dace.float64[N], R: dace.float64[1]):
    R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)


print("Creating SDFG...")
sdfg = simple_reduction.to_sdfg()
sdfg.apply_transformations(GPUTransformMap)
sdfg.simplify()
sdfg.compile()
