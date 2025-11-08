"""
Run with:
python -m fortran_dphpc.maxval_mask
"""
from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
import numpy as np

SQUARE_FORTRAN_SOURCE = """SUBROUTINE minval_test_function(d, res)
integer, dimension(7) :: d
integer, dimension(1) :: dt
integer, dimension(4) :: res

dt = 42

res(1) = MINVAL(d)
res(2) = MINVAL(d(:))
res(3) = MINVAL(d(3:6))
res(4) = MINVAL(dt)

END SUBROUTINE minval_test_function
"""

sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'minval_test_function', True)
sdfg.simplify()

d = np.array([1, 2, 3, 4, 5, 6, 7], dtype=np.int32, order='F')  # Use Fortran ('F') memory order
res = np.zeros([4], dtype=np.int32, order='F')
sdfg(d=d, res=res)

print('result =', res)
