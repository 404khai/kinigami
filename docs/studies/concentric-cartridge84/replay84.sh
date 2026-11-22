#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
CPU=$(python3 -c 'import os;print(min(os.sched_getaffinity(0)))')
run(){ taskset -c "$CPU" python3 -B "$@"; }
run check84.py raw local
run sphere84.py
run interval84.py
run neighbor84.py
run service84.py
run selector84.py
run audit84.py
run witness84.py
run regression84.py
