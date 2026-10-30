//! Minimal minisign signature verifier (standard library only).
//!
//! Used to check the authenticity of the pinned Zig release tarball (Q42,
//! BLD-001) without introducing an external tool. Supports the legacy `Ed`
//! (pure Ed25519) and prehashed `ED` (Ed25519 over BLAKE2b-512) algorithms,
//! and always verifies the global signature over the trusted comment.
//!
//! Usage: zig run tools/minisign.zig -- <public-key-base64> <file> <file.minisig>

const std = @import("std");
const Ed25519 = std.crypto.sign.Ed25519;
const Blake2b512 = std.crypto.hash.blake2.Blake2b512;
const base64 = std.base64.standard.Decoder;

pub const Error = error{
    MalformedPublicKey,
    MalformedSignatureFile,
    UnsupportedAlgorithm,
    KeyIdMismatch,
    BadFileSignature,
    BadTrustedCommentSignature,
};

const trusted_prefix = "trusted comment: ";

fn decodeExact(comptime n: usize, text: []const u8, err: Error) Error![n]u8 {
    const trimmed = std.mem.trim(u8, text, " \t\r");
    const size = base64.calcSizeForSlice(trimmed) catch return err;
    if (size != n) return err;
    var out: [n]u8 = undefined;
    base64.decode(&out, trimmed) catch return err;
    return out;
}

/// Verifies `file_bytes` against a minisign signature file and public key.
/// On success, returns the trusted comment (a slice of `minisig_text`).
pub fn verify(public_key_b64: []const u8, minisig_text: []const u8, file_bytes: []const u8) Error![]const u8 {
    const pk_raw = try decodeExact(42, public_key_b64, error.MalformedPublicKey);
    if (!std.mem.eql(u8, pk_raw[0..2], "Ed")) return error.MalformedPublicKey;
    const public_key = Ed25519.PublicKey.fromBytes(pk_raw[10..42].*) catch return error.MalformedPublicKey;

    var lines = std.mem.splitScalar(u8, minisig_text, '\n');
    const untrusted = lines.next() orelse return error.MalformedSignatureFile;
    if (!std.mem.startsWith(u8, untrusted, "untrusted comment:")) return error.MalformedSignatureFile;
    const sig_raw = try decodeExact(74, lines.next() orelse "", error.MalformedSignatureFile);
    const trusted_line = std.mem.trimEnd(u8, lines.next() orelse "", "\r");
    if (!std.mem.startsWith(u8, trusted_line, trusted_prefix)) return error.MalformedSignatureFile;
    const trusted_comment = trusted_line[trusted_prefix.len..];
    const global_raw = try decodeExact(64, lines.next() orelse "", error.MalformedSignatureFile);

    if (!std.mem.eql(u8, sig_raw[2..10], pk_raw[2..10])) return error.KeyIdMismatch;
    const signature = Ed25519.Signature.fromBytes(sig_raw[10..74].*);

    if (std.mem.eql(u8, sig_raw[0..2], "ED")) {
        var digest: [Blake2b512.digest_length]u8 = undefined;
        Blake2b512.hash(file_bytes, &digest, .{});
        signature.verify(&digest, public_key) catch return error.BadFileSignature;
    } else if (std.mem.eql(u8, sig_raw[0..2], "Ed")) {
        signature.verify(file_bytes, public_key) catch return error.BadFileSignature;
    } else return error.UnsupportedAlgorithm;

    // The global signature covers the file signature plus the trusted comment.
    var global_msg: [64 + 1024]u8 = undefined;
    if (trusted_comment.len > 1024) return error.MalformedSignatureFile;
    @memcpy(global_msg[0..64], sig_raw[10..74]);
    @memcpy(global_msg[64..][0..trusted_comment.len], trusted_comment);
    const global = Ed25519.Signature.fromBytes(global_raw);
    global.verify(global_msg[0 .. 64 + trusted_comment.len], public_key) catch return error.BadTrustedCommentSignature;

    return trusted_comment;
}

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);
    if (args.len != 4) {
        std.debug.print("usage: minisign <public-key-base64> <file> <file.minisig>\n", .{});
        std.process.exit(2);
    }
    const cwd = std.Io.Dir.cwd();
    const file_bytes = try cwd.readFileAlloc(init.io, args[2], arena, .limited(1 << 30));
    const minisig = try cwd.readFileAlloc(init.io, args[3], arena, .limited(1 << 16));
    const trusted = verify(args[1], minisig, file_bytes) catch |err| {
        std.debug.print("minisign: verification FAILED: {s}\n", .{@errorName(err)});
        std.process.exit(1);
    };
    std.debug.print("minisign: signature OK; trusted comment: {s}\n", .{trusted});
}

// --- Tests: sign with a deterministic test key, then verify and tamper. ---

const TestSig = struct { pk_b64: [56]u8, minisig: [400]u8, minisig_len: usize };

fn makeTestSignature(file: []const u8, algorithm: *const [2]u8, comment: []const u8) !TestSig {
    const enc = std.base64.standard.Encoder;
    const kp = try Ed25519.KeyPair.generateDeterministic(@splat(7));
    const key_id = [8]u8{ 1, 2, 3, 4, 5, 6, 7, 8 };

    var pk_raw: [42]u8 = undefined;
    pk_raw[0..2].* = "Ed".*;
    pk_raw[2..10].* = key_id;
    pk_raw[10..42].* = kp.public_key.toBytes();

    var digest: [64]u8 = undefined;
    const message: []const u8 = if (algorithm[1] == 'D') blk: {
        Blake2b512.hash(file, &digest, .{});
        break :blk &digest;
    } else file;
    const sig = try kp.sign(message, null);

    var sig_raw: [74]u8 = undefined;
    sig_raw[0..2].* = algorithm.*;
    sig_raw[2..10].* = key_id;
    sig_raw[10..74].* = sig.toBytes();

    var global_msg: [256]u8 = undefined;
    @memcpy(global_msg[0..64], sig_raw[10..74]);
    @memcpy(global_msg[64..][0..comment.len], comment);
    const global = try kp.sign(global_msg[0 .. 64 + comment.len], null);

    var out: TestSig = undefined;
    _ = enc.encode(&out.pk_b64, &pk_raw);
    var sig_b64: [100]u8 = undefined;
    var glob_b64: [88]u8 = undefined;
    const written = try std.fmt.bufPrint(&out.minisig, "untrusted comment: test\n{s}\ntrusted comment: {s}\n{s}\n", .{
        enc.encode(&sig_b64, &sig_raw), comment, enc.encode(&glob_b64, &global.toBytes()),
    });
    out.minisig_len = written.len;
    return out;
}

test "verifies prehashed and legacy signatures" {
    const file = "kinigami toolchain test payload";
    inline for (.{ "ED", "Ed" }) |alg| {
        const t = try makeTestSignature(file, alg, "timestamp:1\tfile:x");
        const comment = try verify(&t.pk_b64, t.minisig[0..t.minisig_len], file);
        try std.testing.expectEqualStrings("timestamp:1\tfile:x", comment);
    }
}

test "rejects a modified file" {
    const t = try makeTestSignature("original", "ED", "c");
    try std.testing.expectError(error.BadFileSignature, verify(&t.pk_b64, t.minisig[0..t.minisig_len], "originaL"));
}

test "rejects a modified trusted comment" {
    var t = try makeTestSignature("payload", "ED", "file:a");
    const text = t.minisig[0..t.minisig_len];
    const at = std.mem.indexOf(u8, text, "file:a").?;
    text[at + 5] = 'b';
    try std.testing.expectError(error.BadTrustedCommentSignature, verify(&t.pk_b64, text, "payload"));
}

test "rejects a signature from a different key id" {
    const t = try makeTestSignature("payload", "ED", "c");
    var other = t;
    // Re-encode the public key with a different key id but the same key.
    var pk_raw: [42]u8 = undefined;
    _ = try base64.decode(&pk_raw, &t.pk_b64);
    pk_raw[2] ^= 0xff;
    _ = std.base64.standard.Encoder.encode(&other.pk_b64, &pk_raw);
    try std.testing.expectError(error.KeyIdMismatch, verify(&other.pk_b64, t.minisig[0..t.minisig_len], "payload"));
}
