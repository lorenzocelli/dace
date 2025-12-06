"""
Reduction examples using the python frontend of DaCe.

python -m fortran_dphpc.reduce
"""

import os
import numpy as np

import dace

from dace.transformation.dataflow import GPUTransformMap
from dace.transformation.interstate import GPUTransformSDFG

M = dace.symbol("M")
N = dace.symbol("N")


@dace.program
def simple_reduction(A: dace.float64[M, N], R: dace.float64[1]):
    R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)


@dace.program
def simple_masked_reduction_0(
    A: dace.float64[M, N], B: dace.bool[M, N], R: dace.float64[1]
):
    for i, j in dace.map[0:M, 0:N]:
        with dace.tasklet:
            in_A << A[i, j]
            in_B << B[i, j]
            out >> A[i, j]
            if in_B:
                out = in_A
            else:
                out = np.inf
    R[0] = dace.reduce(lambda a, b: min(a, b), A, identity=np.inf)


@dace.program
def simple_masked_reduction_1(
    A: dace.float64[M, N], B: dace.bool[M, N], R: dace.float64[1]
):
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

# Optional: save SDFG to file for inspection
# sdfg.save(os.path.join(os.path.dirname(__file__), "fortran_dphpc_reduce_sdfg.sdfg"))

M = 3000
N = 5000

print("Generating data...")
random = np.random.default_rng(12464)
A = (np.random.rand(M, N) * 10).round().astype(np.float64) + 1.0
B = np.random.rand(M, N) > 0.5
R = np.zeros([1], dtype=np.float64)

exp = np.min(A[B])

print("Running program...")
sdfg(
    A=A,
    B=B,
    R=R,
    M=M,
    N=N,
)

print("A: ", A)
print("B: ", B)
print("R: ", R, " expected: ", exp)
