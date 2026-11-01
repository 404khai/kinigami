# Q50 — Inspector UI library and first 3D view

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-01 |
| Supersedes | — (fills the library choice Q45 left open; INS-002) |
| Provenance | condensed from owner decision ("I'd like to work with zigui … work with that"), adopting the agent's recommendation for the 3D view |

## Context

Q45 chose a native Zig inspector on a vetted graphics library, with sokol named as a candidate only. The owner proposed zigui (`github.com/404khai/zigui`, the owner's fork of `ddalcu/zigui`): a SwiftUI-style 2D UI toolkit in Zig, rendered via SDL3's GPU API with a pure-Zig software fallback. The library review is in `docs/inspector/library-review.md`.

## Decision

1. **zigui is the inspector's UI library.** It provides windows, controls (timeline, play/pause, run and case selection), text, labels, and 2D plots.
2. **First 3D view: wireframe projection drawn with zigui's `Drawing` pen.** Recorded 3D poses are projected to the screen in inspector code and drawn as lines: fixture outlines, tabletop grid, contact points, and force arrows. This adds no further dependency and draws only recorded geometry.
3. **A shaded GPU 3D viewport** (SDL3 GPU rendered offscreen and composited into zigui) is deferred until solid shading or cutaways are needed (INS-010). It requires a later decision.
4. **No browser/WebAssembly inspector in v1.** zigui lists web/WASM as a v1 non-goal. Reopening this requires a new decision.

## Constraints

- zigui and SDL3 stay inspector-only. They never enter the simulation core (Q42, BLD-002), and the core purity check continues to enforce this.
- zigui is pinned by commit and content hash in `build.zig.zon` (BLD-003). Updates are deliberate re-pins.
- **SDL3 is currently an unpinned system library** (Homebrew `sdl3` 3.4.10 on the development host). Until it is vendored or hash-pinned, inspector builds record the SDL3 version, and this is a documented BLD-003 limitation. The inspector is not part of any acceptance evidence, so this does not affect validated results.
- Q45 integrity rules apply unchanged: read-only, recorded values only, unavailable values shown as unavailable, interpolation labeled, and capture never influences results.

## Alternatives considered

- **sokol (C, multi-backend including WebGPU):** keeps a browser path open, but provides no UI toolkit, so controls, text, and layout would have to be built from scratch.
- **A web inspector:** rejected in Q45.
- **A shaded GPU viewport from day one:** more work before anything is visible, and not needed for fixture blocks.
