#!/bin/sh
set -eu
cd "$(dirname "$0")"
export LC_ALL=C OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
for p in plug75 carrier75 lock75 load75 verify75 covers75 assembly75 cut75 mass75 shellwall75; do
  python3 -B "$p.py" > "$p.txt"
done
