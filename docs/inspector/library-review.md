# Inspector library review: zigui (INS-002, Q45, Q50)

Reviewed 2026-11-01 at commit `ad0481f21faa6209d7f04a527996d345e3b7293e` of `github.com/404khai/zigui` (a fork of `ddalcu/zigui`, version 0.2.0).

| Criterion | Finding | Assessment |
| --- | --- | --- |
| License | MIT (code). Bundled fonts: Inter, JetBrains Mono, and Noto Emoji under SIL OFL 1.1. Lucide icons under ISC. Notices are in `assets/fonts/` | Compatible. Attribution must ship with inspector builds |
| Toolchain | `minimum_zig_version = "0.17.0"` | Matches our pin. **Verified:** builds with the pinned compiler (see below) |
| Dependencies | `build.zig.zon` declares none. Core module is pure Zig. Window layer (`src/app.zig`) links system **SDL3** (and `objc` on macOS) | Core: fine. **SDL3 is unpinned**, a BLD-003 limitation (Q50) |
| Architecture fit | Declarative views, `Slider`, `Button`, `List`, `Text`, and a `Drawing` view with a `Pen` (`line`, `fill`, `text`) for custom painting | Fits the controls, plots, and wireframe 3D view |
| 3D | None: 2D canvas only | Wireframe via our own projection (Q50). Shaded 3D deferred |
| Headless | Pure-Zig software rasterizer renders to a framebuffer without a window or GPU | Enables automated, screenshot-checked inspector tests |
| Web / WASM | Explicit v1 non-goal (`PRD.md`) | No browser inspector in v1 (Q50) |
| Maintenance | Pre-alpha. Owner controls the fork. Upstream is active | API may change. Pinning plus owner control mitigate this |
| Module exposure | Exports only the core `zigui` module. The SDL app layer is not exported as a module | Kinigami's `build.zig` assembles the app layer from the pinned package's files |
| Read-only integration | The inspector consumes recordings and snapshots only | Enforced by architecture (Q45). zigui never touches `src/core` |

**Conclusion:** adopted for the inspector UI (Q50), with the SDL3 pinning limitation recorded.
