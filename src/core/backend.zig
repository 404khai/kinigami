//! Physics backend interface (Q15, Q41, PHY-010).
//!
//! The project-owned boundary every backend implements: the custom Zig
//! production solver (not yet written; blocked on preregistered validation
//! criteria) and any alternative that later seeks qualification. Validation
//! reference engines never implement this interface in production builds.
//!
//! The interface is deliberately small and grows only as qualified
//! capabilities need it (PHY-015).

const std = @import("std");
const canonical = @import("canonical.zig");

pub const Vec3 = [3]f64;

/// Identity recorded in run provenance.
pub const Identity = struct {
    name: []const u8,
    version: []const u8,
};

/// A validation-only load to apply during the next step (Q46). Only the run
/// harness supplies these, and only in `fixture_validation` runs.
pub const AppliedLoad = struct {
    body_index: u32,
    world_force_n: Vec3,
    world_torque_nm: Vec3,
    world_point_m: Vec3,
};

pub const StepInputs = struct {
    validation_loads: []const AppliedLoad = &.{},
};

/// A solver-native contact output (PHY-005). Loads come from the solver, never
/// from post-hoc estimation. `body_b == null` means the reference tabletop.
pub const ContactReport = struct {
    body_a: u32,
    body_b: ?u32,
    world_point_m: Vec3,
    world_normal: Vec3,
    normal_force_n: f64,
    tangential_force_n: Vec3,
};

pub const StepError = error{ NumericalFailure, InvalidInput, OutOfMemory };
pub const EncodeError = canonical.BufferEncoder.WriteError;

pub const Backend = struct {
    ptr: *anyopaque,
    vtable: *const VTable,

    pub const VTable = struct {
        identity: *const fn (ptr: *anyopaque) Identity,
        /// Advances one fixed physics step of `dt_s` seconds (Q43).
        step: *const fn (ptr: *anyopaque, dt_s: f64, inputs: StepInputs) StepError!void,
        /// Writes the authoritative state in a documented canonical order (DAT-004).
        encodeState: *const fn (ptr: *anyopaque, e: canonical.BufferEncoder) EncodeError!void,
        /// Contacts produced by the most recent step.
        contacts: *const fn (ptr: *anyopaque) []const ContactReport,
    };

    pub fn identity(self: Backend) Identity {
        return self.vtable.identity(self.ptr);
    }
    pub fn step(self: Backend, dt_s: f64, inputs: StepInputs) StepError!void {
        return self.vtable.step(self.ptr, dt_s, inputs);
    }
    pub fn encodeState(self: Backend, e: canonical.BufferEncoder) EncodeError!void {
        return self.vtable.encodeState(self.ptr, e);
    }
    pub fn contacts(self: Backend) []const ContactReport {
        return self.vtable.contacts(self.ptr);
    }
};
