//! Toolchain conformance tests (Q42, Q44).
//!
//! These record how the *pinned* compiler and standard library actually
//! behave. Tests named "lenient" document std behavior that Kinigami's strict
//! JSON layer must override; if a toolchain upgrade changes any of them, the
//! strict layer and DAT requirements must be re-reviewed.

test {
    _ = @import("std_json_test.zig");
    _ = @import("float_parse_test.zig");
    _ = @import("float_contraction_test.zig");
}
