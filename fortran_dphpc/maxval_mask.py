"""
Run with:
python -m fortran_dphpc.maxval_mask
"""
from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
import numpy as np

INPUT_SIZE = 10
OUTPUT_SIZE = 3

SQUARE_FORTRAN_SOURCE = f"""SUBROUTINE minval_test_function(d, res, mask)
integer, dimension({INPUT_SIZE}) :: d
logical, dimension({INPUT_SIZE}) :: mask
integer, dimension({OUTPUT_SIZE}) :: res

res(1) = MINVAL(d, 0, mask)
! res(1) = MINVAL(array, MASK = mask) ! named argument syntax
! res(2) = MINVAL(d(:)) TODO
! res(3) = MINVAL(d(3:6)) TODO

END SUBROUTINE minval_test_function
"""

sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'minval_test_function', True)
sdfg.simplify()

d = np.arange(INPUT_SIZE, dtype=np.int32)
mask = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1], dtype=np.int32)
res = np.zeros([OUTPUT_SIZE], dtype=np.int32, order='F')
sdfg(d=d, res=res, mask=mask)

print('result =', res)

d = np.array([0, 1, 2, 0, 321, 0, 0, 0, 51, 732], dtype=np.int32)
mask = np.array([0, 0, 0, 0, 1, 0, 0, 0, 1, 1], dtype=np.int32)
res = np.zeros([OUTPUT_SIZE], dtype=np.int32, order='F')
sdfg(d=d, res=res, mask=mask)

print('result =', res)
