// Writes everything under src/generated/ (run on every dev and build):
//   figures.ts   the blog's isometric figures, drawn with the vendored Anatomy kit
//   anatomy.css  the kit's stylesheet
//   records.ts   the decision-log index and the criteria register, read from ../docs and ../criteria
// Run: node scripts/generate.mjs
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../vendor/anatomy/iso-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "../..");
const OUT = join(HERE, "../src/generated");

const W = 640;
const H = 400;
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const T = (at, z, P, text, opts) => k.faceTextSvg(k.topMatrix(at, z, P, "x"), text, opts);
const halo = (P, plan, z, h) => `<path class="iso-halo" d="${k.haloOf(plan, z, h, P)}"/>`;

/** A plate with a groove, corner screws and feet: the bench every figure stands on. */
function bench(P, plan, h) {
  const out = [halo(P, plan, 0, h)];
  for (const [cx, cy] of k.corners(plan, 10)) out.push(S(k.cylinder(cx, cy, 4, -4, 4, P, 20), { tone: "lo" }));
  out.push(S(k.slabOf(plan, 0, h, P, 8, 1.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(plan, 4), h, P), { tone: "faint" }));
  out.push(k.dotsSvg(k.corners(plan, 9).map(([x, y]) => k.iso([x, y, h], P)), { size: 0.55, tone: "mid" }));
  return out.join("");
}

/** A raised block with an inset groove and an engraved label. */
function block(P, plan, z, h, { label, sub, tone = "hi", lit = false, size = 6 } = {}) {
  const out = [S(k.slabOf(plan, z, h, P, 6, 0.8), { tone, lit })];
  if (plan.w > 16 && plan.d > 16) out.push(L(k.planOutline(k.insetPlan(plan, 3), z + h, P), { tone: "faint" }));
  if (label) out.push(T([plan.x + 5, plan.y + plan.d / 2 + size * 0.2], z + h, P, label, { size, tone: "hi" }));
  if (sub) out.push(T([plan.x + 5, plan.y + plan.d / 2 + size * 1.25], z + h, P, sub, { size: size * 0.7, tone: "mid" }));
  return out.join("");
}

/** Paint back to front: items carry a world point, nearer ones are drawn last. */
const painted = (P, items) => items.sort((a, b) => k.depthOf(a.at, P) - k.depthOf(b.at, P)).map((i) => i.svg).join("");

/**
 * Q43. An integer tick ruler with a post at every physics boundary. A message lands on its own
 * tick; a sensor reads the last completed boundary; a command waits for the next one.
 */
function clock() {
  const base = { x: -210, y: -46, w: 420, d: 92, r: 8 };
  const rail = { x: -200, y: -6, w: 400, d: 30, r: 3 };
  const P = k.fitProjection([...k.boxCorners(base, -4, 70)], W, H, { pad: 34 });
  const out = [bench(P, base, 10)];
  out.push(S(k.slabOf(rail, 10, 8, P, 6, 0.6), { tone: "hi" }));
  // ticks hang from the rail's back edge: one per tick, a long one at each physics boundary
  const t = k.topTicks(-195, 195, 10, 5, rail.y, 18, [5, 10], P, "x");
  out.push(L(t.minor, { tone: "lo" }), L(t.major, { tone: "mid" }));
  out.push(T([-196, rail.y + 24], 18, P, "t ∈ ℤ  ·  ONE TICK = ONE TIME UNIT", { size: 5.2, tone: "mid" }));

  const items = [];
  // physics boundaries: posts behind the rail
  for (let x = -150; x <= 150; x += 50) {
    const done = x <= 50;
    items.push({
      at: [x, -26, 10],
      svg: S(k.cylinder(x, -26, 4.5, 10, 46, P, 24, 0.6), { tone: done ? "mid" : "lo" }) + S(k.cylinder(x, -26, 6.5, 56, 3, P, 24, 0.4), { tone: done ? "hi" : "lo" }),
    });
  }
  // events sit on the rail at their exact tick
  const ev = (x, label, tone, lit = false) => ({
    at: [x, 9, 18],
    svg: block(P, { x: x - 7, y: 1, w: 14, d: 20, r: 2 }, 18, lit ? 16 : 10, { tone, lit }) + T([x - 5, 14], lit ? 34 : 28, P, label, { size: 4.6, tone: "hi" }),
  });
  items.push(ev(-130, "MSG", "hi"));
  items.push(ev(-70, "SNS", "hi"));
  items.push(ev(20, "CMD", "hi"));
  items.push(ev(50, "ACT", "hi", true));
  out.push(painted(P, items));
  // the sensor reads the most recent completed boundary; the command takes effect at the next one
  out.push(k.wireSvg(k.iso([-70, 9, 28], P), k.iso([-100, -26, 59], P), { tone: "mid", dotted: true }));
  out.push(k.wireSvg(k.iso([20, 9, 28], P), k.iso([50, 9, 34], P), { tone: "hi", dashed: true, flow: true, via: [k.iso([35, 9, 44], P)] }));
  out.push(T([-196, 36], 10, P, "ORDER = (TICK, PHASE, SOURCE, SEQUENCE)", { size: 6, tone: "hi" }));
  return k.figureSvg({ width: W, height: H, label: "An integer tick ruler: events land on exact ticks, sensors read the last completed physics step, commands wait for the next", body: out });
}

/**
 * Q32. Ground truth on one side of a wall, a controller on the other. The only ways through
 * are ports: sensors, own actuators and couplers, and modeled messages.
 */
function boundary() {
  const base = { x: -200, y: -90, w: 400, d: 180, r: 10 };
  const P = k.fitProjection([...k.boxCorners(base, -4, 90)], W, H, { pad: 30 });
  const out = [bench(P, base, 10)];
  const truth = { x: -186, y: -70, w: 150, d: 140, r: 6 };
  const ctrl = { x: 50, y: -40, w: 130, d: 96, r: 6 };
  const wall = { x: -14, y: -84, w: 10, d: 168, r: 1 };
  const evalr = { x: -186, y: -84, w: 70, d: 10, r: 2 };
  const items = [];
  items.push({ at: [-111, 0, 10], svg: block(P, truth, 10, 14, { label: "GROUND TRUTH", sub: "poses · contacts · loads", size: 8 }) + k.dotsSvg(k.dotGrid(-176, -40, 13, 7, 11, 24, P), { size: 0.5, tone: "lo" }) });
  items.push({ at: [-151, -79, 10], svg: block(P, evalr, 10, 40, { tone: "mid" }) });
  items.push({ at: [-9, 0, 10], svg: S(k.slabOf(wall, 10, 62, P, 4, 0.6), { tone: "hi" }) });
  items.push({ at: [115, 8, 10], svg: block(P, ctrl, 10, 12, { label: "CONTROLLER", sub: "own state · memory", size: 8 }) });
  // ports through the wall
  const ports = [-50, 0, 50];
  ports.forEach((y) => {
    items.push({ at: [-9, y, 40], svg: S(k.slabOf({ x: -18, y: y - 7, w: 18, d: 14, r: 2 }, 36, 12, P, 4, 0.4), { tone: "hi", lit: y === 0 }) });
  });
  out.push(painted(P, items));
  out.push(T([-184, -70], 50, P, "EVALUATOR", { size: 5, tone: "hi" }));
  const labels = ["SENSORS", "MESSAGES", "OWN ACTUATORS"];
  ports.forEach((y, i) => {
    out.push(k.wireSvg(k.iso([-60, y * 0.8, 24], P), k.iso([-18, y, 42], P), { tone: "mid" }));
    out.push(k.wireSvg(k.iso([0, y, 42], P), k.iso([70, y * 0.5 + 8, 22], P), { tone: i === 1 ? "hi" : "mid", dashed: i === 1, flow: i === 1 }));
  });
  labels.forEach((l, i) => out.push(T([62, -32 + i * 9], 22, P, `${String(i + 1).padStart(2, "0")} ${l}`, { size: 5, tone: "mid" })));
  out.push(T([-186, 84], 10, P, "NO PORT FOR POSE, TOPOLOGY OR GLOBAL STATE", { size: 6, tone: "hi" }));
  return k.figureSvg({ width: W, height: H, label: "Ground truth stays on the evaluator's side of a wall; the controller sees only sensors, messages and its own actuators", body: out });
}

/** Q39 and Q78–Q80. Three registered criteria files in a rack, each sealed by its hash; the run reads only the newest. */
function register() {
  const base = { x: -200, y: -80, w: 400, d: 160, r: 10 };
  const P = k.fitProjection([...k.boxCorners(base, -4, 80)], W, H, { pad: 30 });
  const out = [bench(P, base, 10)];
  const files = [
    { v: "v1", hash: "26B2F8DC", note: "CONTRADICTED ITSELF" },
    { v: "v2", hash: "85AE950F", note: "FACE-FACE ONLY" },
    { v: "v3", hash: "05C3D2EC", note: "MIDPLANE" },
  ];
  const items = [];
  files.forEach((f, i) => {
    const x = -184 + i * 92;
    const plan = { x, y: -60, w: 80, d: 104, r: 4 };
    const last = i === files.length - 1;
    const z = 10;
    const h = last ? 16 : 8;
    let svg = block(P, plan, z, h, { tone: last ? "hi" : "mid", lit: last });
    svg += T([x + 6, -46], z + h, P, `CRITERIA ${f.v}`, { size: 6.5, tone: "hi" });
    svg += T([x + 6, -36], z + h, P, `SHA-256 ${f.hash}…`, { size: 4.6, tone: "mid" });
    svg += L(k.lineOnTop([x + 6, -30], [x + 74, -30], z + h, P), { tone: "faint" });
    svg += T([x + 6, -20], z + h, P, f.note, { size: 4.4, tone: last ? "hi" : "mid" });
    // the seal: a stamped disc on each file
    svg += S(k.cylinder(x + 58, 24, 10, z + h, 2, P, 28, 0.4), { tone: last ? "hi" : "lo", lit: last });
    svg += L(k.ring(x + 58, 24, 6.5, z + h + 2, P), { tone: last ? "hi" : "lo" });
    items.push({ at: [x + 40, -8, z], svg });
  });
  const run = { x: 110, y: -10, w: 70, d: 70, r: 6 };
  items.push({ at: [145, 25, 10], svg: block(P, run, 10, 26, { label: "RUN 2", sub: "reads v3 only", size: 7 }) });
  out.push(painted(P, items));
  out.push(k.wireSvg(k.iso([52, 14, 28], P), k.iso([120, 20, 36], P), { tone: "hi", dashed: true, flow: true }));
  out.push(T([-184, 72], 10, P, "REGISTERED BEFORE THE RUN · NEVER EDITED IN PLACE", { size: 6, tone: "hi" }));
  return k.figureSvg({ width: W, height: H, label: "Three versions of the body-contact criteria, each sealed by its SHA-256; the second run reads only version 3", body: out });
}

/**
 * Q73, Q84. A schematic of the packing problem: one round cavity of radius 20, filled by the
 * parts every Kin needs before the coupler gets any room. Not cand-a's geometry.
 */
function cavity() {
  const R = 100; // drawn radius, standing for r 20 mm
  const base = { x: -170, y: -150, w: 340, d: 300, r: 12 };
  const P = k.fitProjection([...k.boxCorners(base, -4, 110)], W, H, { pad: 26 });
  const out = [bench(P, base, 10)];
  out.push(L(k.ring(0, 0, R, 10, P, 64), { tone: "mid" }));
  out.push(L(k.ring(0, 0, R, 92, P, 64), { tone: "lo", dashed: true }));
  const items = [];
  // cell: the largest round part
  items.push({ at: [-30, -20, 10], svg: S(k.cylinder(-30, -20, 34, 10, 54, P, 40, 1), { tone: "hi" }) + T([-52, -18], 64, P, "CELL", { size: 7, tone: "hi" }) });
  // controller board, flat
  items.push({ at: [40, -50, 10], svg: block(P, { x: 14, y: -76, w: 50, d: 40, r: 3 }, 10, 6, { label: "MCU", size: 6 }) + k.dotsSvg(k.dotGrid(20, -70, 6, 2, 7, 16, P), { size: 0.45, tone: "mid" }) });
  // three motors
  [[45, 10], [10, 55], [-55, 45]].forEach(([x, y], i) => {
    items.push({ at: [x, y, 10], svg: S(k.cylinder(x, y, 13, 10, 40, P, 28, 0.8), { tone: "mid" }) + S(k.cylinder(x, y, 4, 50, 8, P, 16), { tone: "hi" }) + T([x - 9, y + 2], 50, P, `M${i + 1}`, { size: 5, tone: "hi" }) });
  });
  // roll-in, yaw and keeper mechanisms
  items.push({ at: [70, -10, 10], svg: block(P, { x: 62, y: -30, w: 18, d: 30, r: 2 }, 10, 30, { tone: "mid" }) });
  items.push({ at: [-75, -5, 10], svg: block(P, { x: -88, y: -10, w: 20, d: 22, r: 2 }, 10, 24, { tone: "mid" }) });
  // the coupler: what is left
  items.push({ at: [62, 54, 10], svg: block(P, { x: 52, y: 44, w: 20, d: 20, r: 2 }, 10, 40, { tone: "hi", lit: true }) });
  out.push(painted(P, items));
  out.push(T([-160, 138], 10, P, "SCHEMATIC · r ≤ 20 MM · CELL, MCU, 3 MOTORS, 3 MECHANISMS", { size: 6, tone: "hi" }));
  out.push(T([46, 74], 10, P, "COUPLER", { size: 5.5, tone: "hi" }));
  return k.figureSvg({ width: W, height: H, label: "Schematic of the packing problem: a cell, controller, three motors and three mechanisms leave the coupler the last corner of a 40 mm cavity", body: out });
}

/** "# Q84 — Title" plus the Status and Recorded rows of the record's header table. */
function decisions() {
  const dir = join(ROOT, "docs/decisions");
  return readdirSync(dir)
    .filter((f) => /^Q\d{3}-/.test(f) && !f.startsWith("Q001-Q030"))
    .sort()
    .map((file) => {
      const text = readFileSync(join(dir, file), "utf8");
      const head = text.match(/^# (Q\d+)\s+—\s+(.+)$/m);
      const row = (name) => text.match(new RegExp(`^\\|\\s*${name}\\s*\\|\\s*([^|]+?)\\s*\\|`, "m"))?.[1];
      if (!head) throw new Error(`${file}: no "# Q<n> — title" heading`);
      return { id: head[1], title: head[2].trim(), status: row("Status") ?? "", recorded: row("Recorded") ?? "", file };
    });
}

/** One row per registered criteria file. */
function register_rows() {
  const text = readFileSync(join(ROOT, "criteria/REGISTER.md"), "utf8");
  return text
    .split("\n")
    .filter((l) => /^\| `[^`]+\.json` \|/.test(l))
    .map((l) => {
      const c = l.split("|").map((s) => s.trim());
      return { file: c[1].replace(/`/g, ""), sha256: c[2].replace(/`/g, ""), date: c[4] };
    });
}

mkdirSync(OUT, { recursive: true });
const figures = { clock: clock(), boundary: boundary(), register: register(), cavity: cavity() };
writeFileSync(
  join(OUT, "figures.ts"),
  `// Generated by scripts/generate.mjs. Do not edit.\nexport const figures = ${JSON.stringify(figures)} as const;\nexport type FigureId = keyof typeof figures;\n`,
);
writeFileSync(join(OUT, "anatomy.css"), `/* Generated from the Anatomy kit's ISO_CSS. Do not edit. */\n${k.ISO_CSS}\n`);
const log = decisions();
const reg = register_rows();
writeFileSync(
  join(OUT, "records.ts"),
  `// Generated by scripts/generate.mjs from docs/decisions and criteria/REGISTER.md. Do not edit.\n` +
    `export type Decision = { id: string; title: string; status: string; recorded: string; file: string };\n` +
    `export type Registered = { file: string; sha256: string; date: string };\n` +
    `export const DECISIONS: Decision[] = ${JSON.stringify(log, null, 1)};\n` +
    `export const REGISTER: Registered[] = ${JSON.stringify(reg, null, 1)};\n`,
);
console.log(`wrote ${Object.keys(figures).join(", ")}; ${log.length} decisions; ${reg.length} registered criteria`);
