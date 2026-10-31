#!/usr/bin/env bash
# Fetch and verify the pinned Zig compiler (Q42, BLD-001).
#
# The compiler identity is the SHA-256 of the official release tarball, as
# published in https://ziglang.org/download/index.json at pin time. The
# tarball is re-verified on every download; extraction happens only after
# the hash matches. Prints the path of the verified `zig` binary.
set -euo pipefail

ZIG_VERSION="0.17.0"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
toolchain_dir="${repo_root}/.toolchain"

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64)  platform="aarch64-macos"; sha256="b607e9b9234790a008116ae5bdb71c6243b84b9fb42a53a9e70fde41c06c536a" ;;
  Darwin-x86_64) platform="x86_64-macos";  sha256="4f9a1c5269aa17ebda5e6d3c2b89d6cbf36f7d2b22a0306e9ab98f25f95529c6" ;;
  Linux-x86_64)  platform="x86_64-linux";  sha256="1cbe9df9f27e6b78d14ccbca43b6703a404ef79ef1c463de901d7f088d4e2026" ;;
  Linux-aarch64) platform="aarch64-linux"; sha256="9e8d11661d4ae3bd57702a3832781e23ad151dde5798e16a5ccd503f65234ff8" ;;
  *) echo "zig-toolchain: unsupported host $(uname -s)-$(uname -m)" >&2; exit 1 ;;
esac

name="zig-${platform}-${ZIG_VERSION}"
install_dir="${toolchain_dir}/${name}"
stamp="${install_dir}/.kinigami-verified-sha256"

sha256_of() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d' ' -f1
  else sha256sum "$1" | cut -d' ' -f1; fi
}

if [[ -x "${install_dir}/zig" && -f "${stamp}" && "$(cat "${stamp}")" == "${sha256}" ]]; then
  echo "${install_dir}/zig"
  exit 0
fi

mkdir -p "${toolchain_dir}"
tarball="${toolchain_dir}/${name}.tar.xz"
url="https://ziglang.org/download/${ZIG_VERSION}/${name}.tar.xz"

echo "zig-toolchain: downloading ${url}" >&2
curl -fsSL --retry 3 -o "${tarball}.part" "${url}"
actual="$(sha256_of "${tarball}.part")"
if [[ "${actual}" != "${sha256}" ]]; then
  rm -f "${tarball}.part"
  echo "zig-toolchain: SHA-256 mismatch for ${name}" >&2
  echo "  expected ${sha256}" >&2
  echo "  actual   ${actual}" >&2
  exit 1
fi
mv "${tarball}.part" "${tarball}"

rm -rf "${install_dir}"
tar -xJf "${tarball}" -C "${toolchain_dir}"
reported="$("${install_dir}/zig" version)"
if [[ "${reported}" != "${ZIG_VERSION}" ]]; then
  echo "zig-toolchain: extracted compiler reports '${reported}', expected '${ZIG_VERSION}'" >&2
  exit 1
fi
echo "${sha256}" > "${stamp}"
echo "zig-toolchain: verified ${name} (sha256 ${sha256})" >&2
echo "${install_dir}/zig"
