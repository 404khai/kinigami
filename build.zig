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

    // Analytic fixture-validation runner (Q46-Q48). Results are labeled
    // `fixture`; provenance (revision, dirty tree, target) is baked in.
    // Provenance is captured by steps that rerun on every build, never by the
    // cached build configuration, so a report can't carry a stale revision.
    const build_info = b.addOptions();
    build_info.addOption([]const u8, "target", target.result.zigTriple(b.allocator) catch "unknown");
    const rev_cmd = b.addSystemCommand(&.{ "git", "rev-parse", "HEAD" });
    rev_cmd.has_side_effects = true;
    const status_cmd = b.addSystemCommand(&.{ "git", "status", "--porcelain" });
    status_cmd.has_side_effects = true;
    const validate_exe = b.addExecutable(.{
        .name = "kinigami-validate",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/validate/main.zig"),
            .target = target,
            .optimize = optimize,
            .imports = &.{
                .{ .name = "kinigami_core", .module = core },
                .{ .name = "build_info", .module = build_info.createModule() },
            },
        }),
    });
    validate_exe.root_module.addAnonymousImport("git_revision", .{ .root_source_file = rev_cmd.captureStdOut(.{}) });
    validate_exe.root_module.addAnonymousImport("git_status", .{ .root_source_file = status_cmd.captureStdOut(.{}) });
    b.installArtifact(validate_exe);
    const validate_run = b.addRunArtifact(validate_exe);
    validate_run.addArgs(&.{"zig-out/fixture-validation-report.json"});
    validate_run.has_side_effects = true;
    b.step("validate", "Run the analytic fixture-validation suite (results labeled fixture)").dependOn(&validate_run.step);

    // Inspector (Q45, Q50): read-only viewer on zigui. zigui and SDL3 are
    // inspector-only dependencies; the simulation core never imports them.
    const zigui_dep = b.dependency("zigui", .{ .target = target, .optimize = optimize });
    const zigui_mod = zigui_dep.module("zigui");
    const inspector_mod = b.createModule(.{
        .root_source_file = b.path("src/inspector/root.zig"),
        .target = target,
        .optimize = optimize,
        .imports = &.{.{ .name = "zigui", .module = zigui_mod }},
    });
    const inspector_tests = b.addTest(.{ .name = "inspector", .root_module = inspector_mod });
    test_step.dependOn(&b.addRunArtifact(inspector_tests).step);

    // zigui exports only its pure-Zig core; its SDL3 window layer is
    // assembled here from the pinned package's files.
    const sdl3_prefix: ?[]const u8 = b.option([]const u8, "sdl3-prefix", "SDL3 install prefix (default: Homebrew on macOS)") orelse
        (if (@import("builtin").os.tag == .macos) "/opt/homebrew/opt/sdl3" else null);
    const sdl_c = b.addTranslateC(.{
        .root_source_file = zigui_dep.path("src/sdl_c.h"),
        .target = target,
        .optimize = optimize,
        .link_libc = true,
    });
    const zigui_app = b.createModule(.{
        .root_source_file = zigui_dep.path("src/app.zig"),
        .target = target,
        .optimize = optimize,
        .link_libc = true,
        .imports = &.{.{ .name = "zigui", .module = zigui_mod }},
    });
    zigui_app.addImport("sdl_c", sdl_c.createModule());
    if (sdl3_prefix) |p| {
        zigui_app.addIncludePath(.{ .cwd_relative = b.fmt("{s}/include", .{p}) });
        zigui_app.addLibraryPath(.{ .cwd_relative = b.fmt("{s}/lib", .{p}) });
        zigui_app.addRPath(.{ .cwd_relative = b.fmt("{s}/lib", .{p}) });
        sdl_c.addIncludePath(.{ .cwd_relative = b.fmt("{s}/include", .{p}) });
    }
    zigui_app.linkSystemLibrary("SDL3", .{});
    if (target.result.os.tag == .macos) zigui_app.linkSystemLibrary("objc", .{});
    const inspector_exe = b.addExecutable(.{
        .name = "kinigami-inspector",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/inspector/main.zig"),
            .target = target,
            .optimize = optimize,
            .link_libc = true,
            .imports = &.{
                .{ .name = "zigui", .module = zigui_mod },
                .{ .name = "zigui_app", .module = zigui_app },
                .{ .name = "inspector", .module = inspector_mod },
                .{ .name = "kinigami_core", .module = core },
            },
        }),
    });
    const install_inspector = b.addInstallArtifact(inspector_exe, .{});
    b.step("inspector", "Build the read-only inspector").dependOn(&install_inspector.step);
    const run_inspector = b.addRunArtifact(inspector_exe);
    run_inspector.addPassthruArgs();
    b.step("run-inspector", "Run the inspector (pass args after --)").dependOn(&run_inspector.step);

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
