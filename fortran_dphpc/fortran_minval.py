"""
Run with:
python -m fortran_dphpc.fortran_minval
"""
from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
from dace.transformation.interstate import GPUTransformSDFG
import numpy as np

SQUARE_FORTRAN_SOURCE = """SUBROUTINE minval_full(d, res)
double precision, dimension(2048) :: d
double precision, dimension(1) :: res

res(1) = MINVAL(d)

END SUBROUTINE minval_full
"""

sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'minval_full', True)
sdfg.apply_transformations(GPUTransformSDFG)
sdfg.simplify()

# Instrument the SDFG
# import dace
# for state in sdfg.nodes():
#     state.instrument = dace.InstrumentationType.GPU_Events
#     for node in state.nodes():
#         if isinstance(node, dace.sdfg.nodes.MapEntry):
#             node.instrument = dace.InstrumentationType.GPU_Events

sdfg.compile()
