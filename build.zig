const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Simulation core: Zig standard library only (Q42, BLD-002).
    const core = b.addModule("kinigami_core", .{
        .root_source_file = b.path("src/core/root.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Preregistered criteria embedded into the core so their consistency is
    // checked on every build (Q39, Q48).
    core.addAnonymousImport("criteria_analytic_v1", .{
        .root_source_file = b.path("criteria/fixture-validation/analytic-v1.json"),
    });

    const test_step = b.step("test", "Run unit tests and toolchain conformance tests");

    const core_tests = b.addTest(.{ .root_module = core });
    test_step.dependOn(&b.addRunArtifact(core_tests).step);

    const purity = b.addSystemCommand(&.{"tools/check-core-purity.sh"});
    purity.has_side_effects = true; // always rescan src/core; never served from cache
    test_step.dependOn(&purity.step);

    // Build tooling (not part of the simulation core).
    const tools_tests = b.addTest(.{
        .name = "tools",
        .root_module = b.createModule(.{
            .root_source_file = b.path("tools/minisign.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    test_step.dependOn(&b.addRunArtifact(tools_tests).step);

    // Toolchain conformance (DAT-005, DAT-007..009, BLD-004): pins down the
    // behavior of the pinned compiler and standard library. Run under every
    // optimization mode, because floating-point contraction and parsing must
    // not depend on it.
    const conformance_step = b.step("conformance", "Run toolchain conformance tests in all optimize modes");
    const modes = [_]std.builtin.OptimizeMode{ .Debug, .ReleaseSafe, .ReleaseFast, .ReleaseSmall };
    for (modes) |mode| {
        const conformance = b.addTest(.{
            .name = b.fmt("conformance-{s}", .{@tagName(mode)}),
            .root_module = b.createModule(.{
                .root_source_file = b.path("tests/conformance/root.zig"),
                .target = target,
                .optimize = mode,
            }),
        });
        const run = b.addRunArtifact(conformance);
        conformance_step.dependOn(&run.step);
        if (mode == optimize) test_step.dependOn(&run.step);
    }
}
