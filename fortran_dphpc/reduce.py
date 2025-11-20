

import numpy as np

import dace

from dace.transformation.dataflow import GPUTransformMap
from dace.transformation.interstate import GPUTransformSDFG

M = dace.symbol('M')
N = dace.symbol('N')


@dace.program
def simple_reduction(A: dace.float64[M, N], B: dace.float64[M, N], C: dace.float64[N]):
    tmp = np.ndarray(shape=[M, N], dtype=np.float64)
    tmp[:] = A[:] + B[:]
    C[:] = dace.reduce(lambda a, b: min(a, b), tmp, axis=0)


sdfg = simple_reduction.to_sdfg()
sdfg.apply_transformations(GPUTransformMap)
sdfg.simplify()

M = 3
N = 5

A = (np.random.rand(M, N) * 10).round().astype(np.float64)
B = (np.random.rand(M, N) * 10).round().astype(np.float64)
C = np.zeros([N], dtype=np.float64) + 1000.0  # TODO C requires initialization

sdfg(A=A, B=B, C=C, M=M, N=N)

print("A + B: ", A + B)
print("C: ", C)
