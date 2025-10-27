# DaCe Fortran Frontend Guide

## Local Setup (macOS)

Other than Python, DaCe requires cmake and the gfortran Fortran compiler. To install cmake on make via homebrew:

```bash
brew install cmake
```

The gfortran compiler can be installed via homebrew as part of the gcc package:

```bash
brew install gcc
```

To use OpenMP with the LLVM/Clang compiler (installed via brew), set the environment variables required by cmake:
```bash
export CC=/opt/homebrew/opt/llvm/bin/clang
export CXX=/opt/homebrew/opt/llvm/bin/clang++
```

⚠️ If you encounter cmake build errors, try deleting the `.dacecache` folder in the root of the repository and run the code again.

## Usage

Here is and example of how to use the Fortran frontend to convert a simple Fortran subroutine that squares the elements of an array.

```python
from dace.frontend.fortran.fortran_parser import create_singular_sdfg_from_string
import numpy as np

SQUARE_FORTRAN_SOURCE = """subroutine square(d, res)
  real, dimension(3) :: d
  real, dimension(3) :: res
  res = d * d
end subroutine square
"""

# 1) Create SDFG (Stateful DataFlow multiGraphs) from the sources. The second arg is the entry-point name.
sdfg = create_singular_sdfg_from_string(SQUARE_FORTRAN_SOURCE, 'square', True)

# 2) Simplify
sdfg.simplify()

# 3) Execute
d = np.array([1, 5, 10.5], dtype=np.float32, order='F')  # Use Fortran ('F') memory order
res = np.zeros([3], dtype=np.float32, order='F')
sdfg(d=d, res=res)

print('result =', res)
```
## How it works

Overview of the steps involved:

1. `create_singular_sdfg_from_string` turns the source into a DaCe SDFG (Stateful DataFlow Graph).
2. `simplify()` applies safe transformations (that will surely increase the performance) on the SDFG.
3. Invoking the SDFG:
    - Compiles the SDFG (`SDFG.compile()`) into an executable in the folder `.dacecache/my_function`. The code is generated with `codegen.generate_code()`.
    - Runs the executable with the provided arguments.
    - Converts the results back to numpy arrays.
