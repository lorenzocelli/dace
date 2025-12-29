"""
Run with:
python -m fortran_dphpc.fortran_minval_dim
"""
from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
import numpy as np

SQUARE_FORTRAN_SOURCE = """SUBROUTINE minval_masked(d, res, mask)
double precision, dimension(2, 3) :: d
logical, dimension(2, 3) :: mask
double precision, dimension(2) :: res

res = MINVAL(d, 2, mask)

END SUBROUTINE minval_masked
"""

sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'minval_masked', True)
sdfg.simplify()

d = np.array([[1.0, 5.0, 3.0],
              [4.0, 2.0, 6.0]],
              dtype=np.double, order='F')
mask = np.ones((3, 3), dtype=np.int32)
res = np.zeros([2], dtype=np.double, order='F')

exp = np.min(d, axis=1)

sdfg(d=d, res=res, mask=mask)

print('result   =', res)
print('expected =', exp)
