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
def simple_masked_reduction_1(
    A: dace.float64[N], B: dace.bool[N], R: dace.float64[1]
):
    # Option 0: tasklet
    # for i, j in dace.map[0:M, 0:N]:
    #     with dace.tasklet:
    #         in_A << A[i, j]
    #         in_B << B[i, j]
    #         out >> A[i, j]
    #         if in_B:
    #             out = in_A
    #         else:
    #             out = np.inf
    # R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)

    # Option 1: map
    # for i, j in dace.map[0:M, 0:N]:
    #    if not B[i, j]:
    #        A[i, j] = np.inf
    # R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)

    # Option 2: inverted mask
    # A[~B] = np.inf
    # R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)

    # Option 3: np.where
    R[0] = dace.reduce(lambda a, b: min(a, b), np.where(B, A, np.inf), identity=np.inf)


print("Creating SDFG...")
sdfg = simple_masked_reduction_1.to_sdfg()
sdfg.apply_transformations(GPUTransformMap)
sdfg.simplify()
sdfg.compile()
