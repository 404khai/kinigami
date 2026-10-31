//! Strict, fail-closed JSON parsing for criteria and configuration files
//! (Q44, DAT-005..008).
//!
//! `std.json.parseFromSlice` is lenient in ways Q44 forbids (recorded in
//! docs/toolchain.md). This layer uses only the std tokenizer and applies
//! every typing rule itself:
//!
//! | JSON input                           | Result                       |
//! | ------------------------------------ | ---------------------------- |
//! | unknown or duplicate object key      | `UnknownField`, `DuplicateField` |
//! | missing field without a default      | `MissingField`               |
//! | string where a number is expected    | `TypeMismatch`               |
//! | `3.0` / `3e0` in an integer field    | `IntegerNotExact`            |
//! | integer with magnitude ≥ 2^53        | `IntegerOutOfRange` (use `StringU64`) |
//! | number outside the target type range | `IntegerOutOfRange`          |
//! | decimal that overflows binary64      | `NonFiniteNumber`            |
//! | `"nan"`, `"inf"` in a float field    | `TypeMismatch` (strings never become numbers) |
//! | number where an enum is expected     | `TypeMismatch`               |
//! | `null` for a non-optional field      | `TypeMismatch`               |
//! | trailing content, malformed input    | tokenizer error              |
//!
//! Accepted on purpose: an integer-formatted number in an `f64` field (`1`
//! becomes `1.0` exactly, under the same correctly rounded conversion).
//!
//! Defaults: a struct field's Zig default value is the schema default. It is
//! used only when the key is absent, and callers must write the resolved
//! value into the effective configuration (DAT-006). Optional fields
//! (`?T`) have no implicit default: an absent optional key is `MissingField`
//! unless the field declares one, so `null` must be written explicitly.

const std = @import("std");
const Scanner = std.json.Scanner;
const Token = std.json.Token;

/// Largest integer magnitude accepted as a JSON number (DAT-007): 2^53 - 1.
pub const max_safe_integer: u64 = (1 << 53) - 1;

pub const SchemaError = error{
    UnknownField,
    DuplicateField,
    MissingField,
    TypeMismatch,
    IntegerNotExact,
    IntegerOutOfRange,
    NonFiniteNumber,
    InvalidEnumTag,
    LengthMismatch,
    InvalidStringInteger,
    TooDeep,
};

pub const Error = SchemaError || Scanner.AllocError;

pub const Options = struct {
    /// Maximum nesting of arrays and objects.
    max_depth: u16 = 64,
};

/// Unsigned 64-bit integer carried as a JSON string of decimal digits
/// (DAT-007), for values that may exceed 2^53 - 1 such as tick counts.
/// Rejects signs, leading zeros, whitespace, and empty strings.
pub const StringU64 = struct {
    value: u64,
};

pub fn Parsed(comptime T: type) type {
    return struct {
        arena: *std.heap.ArenaAllocator,
        value: T,

        pub fn deinit(self: @This()) void {
            const gpa = self.arena.child_allocator;
            self.arena.deinit();
            gpa.destroy(self.arena);
        }
    };
}

/// Parses a complete JSON document into `T`. Strings in the result are owned
/// by the returned arena.
pub fn parse(comptime T: type, gpa: std.mem.Allocator, text: []const u8, options: Options) Error!Parsed(T) {
    const arena = try gpa.create(std.heap.ArenaAllocator);
    errdefer gpa.destroy(arena);
    arena.* = .init(gpa);
    errdefer arena.deinit();

    var scanner = Scanner.initCompleteInput(arena.allocator(), text);
    defer scanner.deinit();
    var p: Parser = .{ .scanner = &scanner, .arena = arena.allocator(), .options = options };
    const value = try p.value(T, try p.next(), 0);
    if (try p.next() != .end_of_document) return error.SyntaxError;
    return .{ .arena = arena, .value = value };
}

const Parser = struct {
    scanner: *Scanner,
    arena: std.mem.Allocator,
    options: Options,

    fn next(self: *Parser) Error!Token {
        return self.scanner.nextAlloc(self.arena, .alloc_if_needed);
    }

    fn value(self: *Parser, comptime T: type, token: Token, depth: u16) Error!T {
        if (T == StringU64) return .{ .value = try parseStringU64(stringOf(token) orelse return error.TypeMismatch) };
        switch (@typeInfo(T)) {
            .bool => return switch (token) {
                .true => true,
                .false => false,
                else => error.TypeMismatch,
            },
            .int => return parseInt(T, numberOf(token) orelse return error.TypeMismatch),
            .float => {
                if (T != f64) @compileError("strict_json supports f64 only");
                return parseF64(numberOf(token) orelse return error.TypeMismatch);
            },
            .@"enum" => {
                const name = stringOf(token) orelse return error.TypeMismatch;
                return std.meta.stringToEnum(T, name) orelse error.InvalidEnumTag;
            },
            .optional => |o| {
                if (token == .null) return null;
                return try self.value(o.child, token, depth);
            },
            .pointer => |ptr| {
                if (ptr.size != .slice) @compileError("unsupported pointer type " ++ @typeName(T));
                if (T == []const u8) return stringOf(token) orelse error.TypeMismatch;
                if (token != .array_begin) return error.TypeMismatch;
                const d = try deeper(self, depth);
                var list: std.ArrayList(ptr.child) = .empty;
                while (true) {
                    const t = try self.next();
                    if (t == .array_end) break;
                    try list.append(self.arena, try self.value(ptr.child, t, d));
                }
                return list.toOwnedSlice(self.arena);
            },
            .array => |arr| {
                if (token != .array_begin) return error.TypeMismatch;
                const d = try deeper(self, depth);
                var out: T = undefined;
                var i: usize = 0;
                while (true) : (i += 1) {
                    const t = try self.next();
                    if (t == .array_end) break;
                    if (i >= arr.len) return error.LengthMismatch;
                    out[i] = try self.value(arr.child, t, d);
                }
                if (i != arr.len) return error.LengthMismatch;
                return out;
            },
            .@"struct" => |st| {
                if (token != .object_begin) return error.TypeMismatch;
                const d = try deeper(self, depth);
                var out: T = undefined;
                var seen: [st.field_names.len]bool = @splat(false);
                while (true) {
                    const key_token = try self.next();
                    if (key_token == .object_end) break;
                    const key = stringOf(key_token) orelse return error.SyntaxError;
                    inline for (st.field_names, st.field_types, 0..) |name, FieldType, i| {
                        if (std.mem.eql(u8, key, name)) {
                            if (seen[i]) return error.DuplicateField;
                            seen[i] = true;
                            @field(out, name) = try self.value(FieldType, try self.next(), d);
                            break;
                        }
                    } else return error.UnknownField;
                }
                inline for (st.field_names, st.field_types, st.field_attrs, 0..) |name, FieldType, attrs, i| {
                    if (!seen[i]) {
                        if (comptime attrs.defaultValue(FieldType)) |default| {
                            @field(out, name) = default;
                        } else return error.MissingField;
                    }
                }
                return out;
            },
            else => @compileError("unsupported type " ++ @typeName(T)),
        }
    }

    fn deeper(self: *Parser, depth: u16) Error!u16 {
        if (depth >= self.options.max_depth) return error.TooDeep;
        return depth + 1;
    }
};

fn numberOf(token: Token) ?[]const u8 {
    return switch (token) {
        .number => |n| n,
        .allocated_number => |n| n,
        else => null,
    };
}

fn stringOf(token: Token) ?[]const u8 {
    return switch (token) {
        .string => |s| s,
        .allocated_string => |s| s,
        else => null,
    };
}

fn parseInt(comptime T: type, text: []const u8) SchemaError!T {
    if (!std.json.isNumberFormattedLikeAnInteger(text)) return error.IntegerNotExact;
    const wide = std.fmt.parseInt(i128, text, 10) catch return error.IntegerOutOfRange;
    if (@abs(wide) > max_safe_integer) return error.IntegerOutOfRange;
    return std.math.cast(T, wide) orelse error.IntegerOutOfRange;
}

fn parseF64(text: []const u8) SchemaError!f64 {
    // The tokenizer has already enforced JSON number grammar, so parseFloat
    // only ever sees decimal syntax (no "nan", "inf", hex, or underscores).
    const v = std.fmt.parseFloat(f64, text) catch return error.TypeMismatch;
    if (!std.math.isFinite(v)) return error.NonFiniteNumber;
    return v;
}

fn parseStringU64(text: []const u8) SchemaError!u64 {
    if (text.len == 0) return error.InvalidStringInteger;
    if (text.len > 1 and text[0] == '0') return error.InvalidStringInteger;
    for (text) |c| if (c < '0' or c > '9') return error.InvalidStringInteger;
    return std.fmt.parseInt(u64, text, 10) catch error.InvalidStringInteger;
}

// --- Tests: every lenient std behavior recorded in docs/toolchain.md must be
// --- rejected here, plus the strict behaviors std already has.

const testing = std.testing;

const Sample = struct {
    count: u32,
    ratio: f64,
    mode: enum { strict, loose },
};

fn expectReject(comptime T: type, expected: anyerror, text: []const u8) !void {
    if (parse(T, testing.allocator, text, .{})) |p| {
        p.deinit();
        std.debug.print("accepted: {s}\n", .{text});
        return error.TestUnexpectedSuccess;
    } else |err| {
        if (err != expected) {
            std.debug.print("{s}: got {s}, expected {s}\n", .{ text, @errorName(err), @errorName(expected) });
            return error.TestUnexpectedError;
        }
    }
}

test "accepts a well-formed document" {
    const p = try parse(Sample, testing.allocator, "{\"count\":3,\"ratio\":0.5,\"mode\":\"loose\"}", .{});
    defer p.deinit();
    try testing.expectEqual(@as(u32, 3), p.value.count);
    try testing.expectEqual(@as(f64, 0.5), p.value.ratio);
    try testing.expectEqual(.loose, p.value.mode);
}

test "lenient 1: numeric strings are rejected in number fields" {
    try expectReject(Sample, error.TypeMismatch, "{\"count\":\"3\",\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectReject(Sample, error.TypeMismatch, "{\"count\":3,\"ratio\":\"0.5\",\"mode\":\"strict\"}");
}

test "lenient 2: float-formatted numbers are rejected in integer fields" {
    try expectReject(Sample, error.IntegerNotExact, "{\"count\":3.0,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectReject(Sample, error.IntegerNotExact, "{\"count\":3e0,\"ratio\":0.5,\"mode\":\"strict\"}");
}

test "lenient 3: integer enum tags are rejected" {
    try expectReject(Sample, error.TypeMismatch, "{\"count\":3,\"ratio\":0.5,\"mode\":1}");
    try expectReject(Sample, error.InvalidEnumTag, "{\"count\":3,\"ratio\":0.5,\"mode\":\"medium\"}");
}

test "lenient 4: non-finite strings are rejected in float fields" {
    try expectReject(Sample, error.TypeMismatch, "{\"count\":3,\"ratio\":\"nan\",\"mode\":\"strict\"}");
    try expectReject(Sample, error.TypeMismatch, "{\"count\":3,\"ratio\":\"-inf\",\"mode\":\"strict\"}");
}

test "lenient 5: decimal overflow is rejected instead of becoming infinity" {
    try expectReject(Sample, error.NonFiniteNumber, "{\"count\":3,\"ratio\":1e400,\"mode\":\"strict\"}");
    try expectReject(Sample, error.NonFiniteNumber, "{\"count\":3,\"ratio\":-1.7976931348623159e308,\"mode\":\"strict\"}");
}

test "lenient 6: integers at or above 2^53 are rejected as JSON numbers" {
    const Wide = struct { tick: u64 };
    const ok = try parse(Wide, testing.allocator, "{\"tick\":9007199254740991}", .{});
    ok.deinit();
    try expectReject(Wide, error.IntegerOutOfRange, "{\"tick\":9007199254740992}");
    try expectReject(Wide, error.IntegerOutOfRange, "{\"tick\":-9007199254740992}");
}

test "lenient 7 (accepted by design): integer literals in f64 fields" {
    const p = try parse(Sample, testing.allocator, "{\"count\":3,\"ratio\":1,\"mode\":\"strict\"}", .{});
    defer p.deinit();
    try testing.expectEqual(@as(f64, 1.0), p.value.ratio);
}

test "StringU64 carries values beyond 2^53 and rejects non-canonical text" {
    const Wide = struct { tick: StringU64 };
    const p = try parse(Wide, testing.allocator, "{\"tick\":\"18446744073709551615\"}", .{});
    defer p.deinit();
    try testing.expectEqual(@as(u64, std.math.maxInt(u64)), p.value.tick.value);
    for ([_][]const u8{ "\"\"", "\"007\"", "\"+1\"", "\"-1\"", "\" 1\"", "\"18446744073709551616\"", "\"1e3\"" }) |v| {
        var buf: [64]u8 = undefined;
        try expectReject(Wide, error.InvalidStringInteger, try std.fmt.bufPrint(&buf, "{{\"tick\":{s}}}", .{v}));
    }
    try expectReject(Wide, error.TypeMismatch, "{\"tick\":5}");
}

test "structural strictness: unknown, duplicate, missing, null, trailing" {
    try expectReject(Sample, error.UnknownField, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\",\"extra\":1}");
    try expectReject(Sample, error.DuplicateField, "{\"count\":3,\"count\":3,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectReject(Sample, error.MissingField, "{\"count\":3,\"mode\":\"strict\"}");
    try expectReject(Sample, error.TypeMismatch, "{\"count\":null,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectReject(Sample, error.SyntaxError, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\"} {}");
    try expectReject(Sample, error.IntegerOutOfRange, "{\"count\":-1,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectReject(Sample, error.TypeMismatch, "[]");
}

test "schema defaults apply only to absent keys; optionals need explicit null" {
    const WithDefault = struct { a: u8, b: u8 = 7, c: ?u8 };
    const p = try parse(WithDefault, testing.allocator, "{\"a\":1,\"c\":null}", .{});
    defer p.deinit();
    try testing.expectEqual(@as(u8, 7), p.value.b);
    try testing.expectEqual(@as(?u8, null), p.value.c);
    try expectReject(WithDefault, error.MissingField, "{\"a\":1}");
}

test "arrays: slices, exact-length arrays, and depth limit" {
    const Arr = struct { xs: []const f64, v: [3]f64 };
    const p = try parse(Arr, testing.allocator, "{\"xs\":[1,2.5],\"v\":[0,0,1]}", .{});
    defer p.deinit();
    try testing.expectEqualSlices(f64, &.{ 1, 2.5 }, p.value.xs);
    try expectReject(Arr, error.LengthMismatch, "{\"xs\":[],\"v\":[0,0]}");
    try expectReject(Arr, error.LengthMismatch, "{\"xs\":[],\"v\":[0,0,0,0]}");
    const Deep = struct { xs: []const []const u8 };
    if (parse(Deep, testing.allocator, "{\"xs\":[]}", .{ .max_depth = 1 })) |d| {
        d.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(error.TooDeep, err);
}

test "escaped strings are decoded" {
    const S = struct { name: []const u8 };
    const p = try parse(S, testing.allocator, "{\"name\":\"a\\u00e9\\n\"}", .{});
    defer p.deinit();
    try testing.expectEqualStrings("a\u{e9}\n", p.value.name);
}
