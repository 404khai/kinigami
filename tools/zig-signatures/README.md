# Zig 0.17.0 release signatures

Official minisign signatures for the pinned tarballs, as published at
`https://ziglang.org/download/0.17.0/<tarball>.minisig` (fetched 2026-10-30).

Zig release signing public key:

```
RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U
```

The key was obtained from two independently hosted sources, and both match:

- `https://ziglang.org/download/` (the download page)
- `https://raw.githubusercontent.com/ziglang/www.ziglang.org/main/content/en-US/download.smd` (the website's source repository on GitHub)

Verify with the repository's std-only verifier (`tools/zig-verify-signature.sh`)
or with the reference `minisign` tool:

```sh
minisign -Vm zig-aarch64-macos-0.17.0.tar.xz -P RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U
```
