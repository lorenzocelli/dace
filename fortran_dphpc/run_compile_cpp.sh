#!/bin/bash
#SBATCH --account=dphpc
#SBATCH --gpus=5060ti:1
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

source /etc/profile
module add cuda/12.8

# Clear previous build
rm -rf build

export CUDACXX=/cluster/data/cuda/12.8.1/bin/nvcc
export PROG_NAME="simple_masked_reduction_1"

mkdir -p build
cd build
cmake  "/home/lcelli/dace/dace/codegen" \
    -DDACE_SRC_DIR="/home/lcelli/dace/.dacecache/$PROG_NAME/src" \
    -DDACE_FILES="cpu/$PROG_NAME.cpp;cuda/${PROG_NAME}_cuda.cu;../sample/${PROG_NAME}_main.cpp" \
    -DDACE_PROGRAM_NAME=$PROG_NAME \
    -DDACE_ENV_CMAKE_FILES="" \
    -DDACE_ENV_COMPILE_FLAGS="" \
    -DDACE_ENV_INCLUDES="" \
    -DDACE_ENV_LIBRARIES="" \
    -DDACE_ENV_MINIMUM_VERSION=0 \
    -DDACE_ENV_PACKAGES="" \
    -DDACE_ENV_VAR_KEYS="" \
    -DDACE_ENV_VAR_VALUES="" \
    -DCMAKE_CXX_FLAGS="-std=c++14 -fPIC -Wall -Wextra -O3 -march=native -ffast-math -Wno-unused-parameter -Wno-unused-label" \
    -DDACE_CUDA_ARCHITECTURES_DEFAULT="60" \
    -DCMAKE_CUDA_FLAGS="-Xcompiler -march=native --use_fast_math -Xcompiler -Wno-unused-parameter" \
    -DDACE_LIBS="" \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--disable-new-dtags"

cmake --build . --config RelWithDebInfo
