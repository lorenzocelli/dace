#!/bin/bash
#SBATCH --account=dphpc
#SBATCH --gpus=5060ti:1
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

source /etc/profile

module add cuda/12.8

nvidia-smi

# Activate virtual environment
source .venv/bin/activate

# Clear DaCe cache to avoid stale data
rm -rf .dacecache

export CUDACXX=/cluster/data/cuda/12.8.1/bin/nvcc
python -m fortran_dphpc.py_minval
