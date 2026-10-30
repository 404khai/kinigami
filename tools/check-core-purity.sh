#!/usr/bin/env bash
# Simulation-core purity check (BLD-002, TIM-007, TIM-009).
#
# The core may import only `std` and its own relative files, and must not
# reach wall-clock time, ambient/OS randomness, threads, or the process
# environment. This is a textual check: it catches accidental use, not a
# determined bypass, and it does not replace review.
set -euo pipefail
core_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/src/core"
status=0

forbidden=(
  'std\.time\b'        # wall-clock time
  'Clock'              # std.Io clocks
  'Timestamp'          # milliTimestamp, nanoTimestamp, ...
  'std\.crypto\.random' # OS entropy
  'std\.Thread\b'      # threads (single-threaded until TIM-009 is verified)
  'getenv|environ'     # process environment
)
for pattern in "${forbidden[@]}"; do
  if grep -rnE "${pattern}" "${core_dir}" --include='*.zig'; then
    echo "core-purity: forbidden pattern '${pattern}' in src/core" >&2
    status=1
  fi
done

# Imports: only "std" or relative .zig files.
if grep -rnoE '@import\("[^"]*"\)' "${core_dir}" --include='*.zig' \
    | grep -vE '@import\("std"\)$|@import\("[A-Za-z0-9_./-]+\.zig"\)$'; then
  echo "core-purity: non-std, non-relative import in src/core" >&2
  status=1
fi

exit "${status}"
