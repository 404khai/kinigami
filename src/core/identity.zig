//! Artifact identity hashes (Q44, DAT-003).
//!
//! A file identity is SHA-256 over the exact file bytes, with no
//! normalization: whitespace or key-order changes produce a new identity.
//! Checkpoint state hashes (DAT-004) are a different thing and are computed
//! over a canonical state encoding, not by this module.

const std = @import("std");
const Sha256 = std.crypto.hash.sha2.Sha256;

pub const digest_length = Sha256.digest_length;
pub const Digest = [digest_length]u8;
pub const HexDigest = [digest_length * 2]u8;

/// SHA-256 over the exact bytes of an artifact.
pub fn fileIdentity(bytes: []const u8) Digest {
    var out: Digest = undefined;
    Sha256.hash(bytes, &out, .{});
    return out;
}

/// Lowercase hexadecimal form used in registers and result provenance.
pub fn toHex(digest: Digest) HexDigest {
    return std.fmt.bytesToHex(digest, .lower);
}

test "fileIdentity matches FIPS 180-2 test vectors" {
    try std.testing.expectEqualStrings(
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        &toHex(fileIdentity("")),
    );
    try std.testing.expectEqualStrings(
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        &toHex(fileIdentity("abc")),
    );
}

test "fileIdentity does not normalize whitespace or key order" {
    const a = fileIdentity("{\"a\":1,\"b\":2}");
    try std.testing.expect(!std.mem.eql(u8, &a, &fileIdentity("{\"a\": 1,\"b\":2}")));
    try std.testing.expect(!std.mem.eql(u8, &a, &fileIdentity("{\"b\":2,\"a\":1}")));
}
