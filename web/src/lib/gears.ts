/**
 * Spur-gear outlines and meshing trains (after cogs' gear lib). Gears are chained by pitch
 * radius (module × teeth / 2) and phased so every tooth sits in its neighbour's gap. Spin each
 * at a period ∝ its teeth, alternating direction, and they stay meshed forever.
 */
export type Pt = [number, number];
export type MeshGear = { z: number; cx: number; cy: number; phase: number; dir: 1 | -1 };

/** Tooth polygon: root, flank, tip, tip, flank per tooth. */
export function gearPoints(cx: number, cy: number, teeth: number, rRoot: number, rTip: number, phase = -Math.PI / 2): Pt[] {
  const T = (Math.PI * 2) / teeth;
  const pts: Pt[] = [];
  const at = (r: number, a: number): Pt => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  for (let i = 0; i < teeth; i++) {
    const c = phase + i * T;
    pts.push(at(rRoot, c - 0.3 * T), at(rTip, c - 0.15 * T), at(rTip, c + 0.15 * T), at(rRoot, c + 0.3 * T), at(rRoot, c + 0.5 * T));
  }
  return pts;
}

export const polyD = (pts: Pt[]) => "M" + pts.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" L") + " Z";

export function meshChain(module: number, start: { z: number; cx: number; cy: number }, links: { z: number; deg: number }[]): MeshGear[] {
  const out: MeshGear[] = [{ ...start, phase: 0, dir: 1 }];
  for (const l of links) {
    const a = out[out.length - 1];
    const ra = (module * a.z) / 2;
    const rb = (module * l.z) / 2;
    const phi = (l.deg * Math.PI) / 180;
    const ta = (Math.PI * 2) / a.z;
    const tb = (Math.PI * 2) / l.z;
    const delta = (((a.phase - phi) % ta) + ta) % ta;
    out.push({
      z: l.z,
      cx: a.cx + (ra + rb) * Math.cos(phi),
      cy: a.cy + (ra + rb) * Math.sin(phi),
      phase: phi + Math.PI - (delta / ta + 0.5) * tb,
      dir: (a.dir * -1) as 1 | -1,
    });
  }
  return out;
}
