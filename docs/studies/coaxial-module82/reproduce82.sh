#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
CPU=$(python3 -c 'import os;print(min(os.sched_getaffinity(0)))')
run(){ taskset -c "$CPU" python3 -B "$@"; }
run check82.py local sphere pairs >/dev/null
run audit82.py
run neighbor82.py
run regression82.py
