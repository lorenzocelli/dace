

import numpy as np

import dace

from dace.transformation.dataflow import GPUTransformMap
from dace.transformation.interstate import GPUTransformSDFG

M = dace.symbol('M')
N = dace.symbol('N')


@dace.program
def simple_reduction(A: dace.float64[M, N], R: dace.float64[1]):
    R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)


sdfg = simple_reduction.to_sdfg()
sdfg.apply_transformations(GPUTransformMap)
sdfg.simplify()

M = 3
N = 5

A = (np.random.rand(M, N) * 10).round().astype(np.float64) + 1.0
R = np.zeros([1], dtype=np.float64)

sdfg(A=A, R=R, M=M, N=N)

print("A: ", A)
print("R: ", R, " expected: ", np.min(A))
