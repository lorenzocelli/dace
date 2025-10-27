from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
import numpy as np

INPUT_SIZE = 500
OUTPUT_SIZE = 3

SQUARE_FORTRAN_SOURCE = f"""SUBROUTINE minval_test_function(d, res, mask)
integer, dimension({INPUT_SIZE}) :: d
logical, dimension({INPUT_SIZE}) :: mask
integer, dimension({OUTPUT_SIZE}) :: res

res(1) = MINVAL(d, mask=mask)
res(2) = MINVAL(d(:), mask=mask)
res(3) = MINVAL(d(3:6), mask=mask)

END SUBROUTINE minval_test_function
"""

sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'minval_test_function', True)
sdfg.simplify()

d = np.arange(INPUT_SIZE, dtype=np.int32)
mask = np.random.rand(INPUT_SIZE) > 0.5
res = np.zeros([OUTPUT_SIZE], dtype=np.int32, order='F')
sdfg(d=d, res=res, mask=mask)

print('result =', res)
