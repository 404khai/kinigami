#!/usr/bin/env bash
# Verify the downloaded pinned Zig tarball against its official minisign
# signature (tools/zig-signatures/). The verifier runs under the pinned
# compiler itself, so this check is only as trustworthy as the SHA-256 pin
# that admitted that compiler; for an independent check use the reference
# `minisign` tool (see tools/zig-signatures/README.md).
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
public_key="RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U"
zig_bin="$("${repo_root}/tools/zig-toolchain.sh")"
name="$(basename "$(dirname "${zig_bin}")")"
cd "${repo_root}"
exec "${zig_bin}" run tools/minisign.zig -- "${public_key}" ".toolchain/${name}.tar.xz" "tools/zig-signatures/${name}.tar.xz.minisig"
