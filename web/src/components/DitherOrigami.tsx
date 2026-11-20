import { useEffect, useRef, useState, type RefObject } from "react";
import { SHAPES, type Pt, type ShapeKind } from "../lib/origami";

/**
 * Ordered-dither (Bayer 8×8) origami, after graft's DitherTree: each frame paints a small
 * greyscale scene of folded-paper creatures, one flat grey per facet so the creases read
 * through the dot density, then prints it as square dots in each creature's own ink.
 * Creatures unfold facet by facet on first sight, bob gently, pause off screen, and hold
 * still under prefers-reduced-motion.
 */

export type Creature = {
  kind: ShapeKind;
  /** centre, as fractions of the field */
  x: number;
  y: number;
  /** half-height of the unit shape, as a fraction of the field height */
  size: number;
  ink: string;
  /** resting tilt in radians */
  tilt?: number;
  /** mirror horizontally */
  flip?: boolean;
  seed?: number;
};

const BAYER = (() => {
  const m = [
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
  ];
  return m.map((row) => row.map((v) => (v + 0.5) / 64));
})();

function useVisible(ref: RefObject<Element | null>) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(([e]) => setOn(e.isIntersecting), { rootMargin: "120px" });
    io.observe(el);
    return () => io.disconnect();
  }, [ref]);
  return on;
}

export function DitherOrigami({
  creatures,
  cell = 4,
  light = 0.25,
  fade,
  className,
}: {
  creatures: Creature[];
  /** dot pitch in CSS px */
  cell?: number;
  /** strength of the travelling light, 0–1 */
  light?: number;
  /** keep a reading area quiet: an ellipse centre and radii as fractions */
  fade?: { x: number; y: number; rx: number; ry: number };
  className?: string;
}) {
  const host = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const visible = useVisible(host);
  const born = useRef<number | null>(null);

  useEffect(() => {
    const out = canvas.current;
    const octx = out?.getContext("2d");
    if (!out || !octx) return;
    const scene = document.createElement("canvas");
    const sctx = scene.getContext("2d", { willReadFrequently: true });
    if (!sctx) return;
    const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    let frame = 0;

    const draw = (now: number) => {
      const box = out.getBoundingClientRect();
      const dpr = Math.min(devicePixelRatio || 1, 2);
      const cols = Math.max(1, Math.floor(box.width / cell));
      const rows = Math.max(1, Math.floor(box.height / cell));
      if (scene.width !== cols || scene.height !== rows) {
        scene.width = cols;
        scene.height = rows;
      }
      if (out.width !== Math.round(box.width * dpr) || out.height !== Math.round(box.height * dpr)) {
        out.width = Math.round(box.width * dpr);
        out.height = Math.round(box.height * dpr);
      }
      if (born.current === null) born.current = now;
      const t = reduced ? 1e4 : (now - born.current) / 1000;
      const lx = ((Math.sin(t * 0.3) + 1) / 2) * cols;

      octx.setTransform(1, 0, 0, 1, 0, 0);
      octx.clearRect(0, 0, out.width, out.height);
      const step = cell * dpr;
      const dot = Math.max(1, step - Math.max(1, dpr));

      // One pass per creature, so each prints in its own ink and edges never borrow a neighbour's.
      creatures.forEach((c, ci) => {
        // 1. scene: brightness = ink density
        sctx.fillStyle = "#000";
        sctx.fillRect(0, 0, cols, rows);
        const facets = SHAPES[c.kind];
        const seed = c.seed ?? ci * 1.7;
        const unfold = reduced ? facets.length : Math.min(facets.length, Math.max(0, (t - 0.15 * ci) * 4.5));
        const s = rows * c.size;
        const bob = reduced ? 0 : Math.sin(t * 0.8 + seed) * 0.025 * s;
        const rot = (c.tilt ?? 0) + (reduced ? 0 : Math.sin(t * 0.5 + seed) * 0.04);
        const cx = cols * c.x;
        const cy = rows * c.y + bob;
        const cos = Math.cos(rot);
        const sin = Math.sin(rot);
        const map = ([px, py]: Pt): Pt => {
          const x = (c.flip ? -px : px) * s;
          const y = py * s;
          return [cx + x * cos - y * sin, cy + x * sin + y * cos];
        };
        facets.forEach((f, fi) => {
          const k = Math.min(1, unfold - fi);
          if (k <= 0) return;
          // unfold from the facet's first vertex, its hinge
          const hinge = f.pts[0];
          const pts = f.pts.map(([x, y]) => map([hinge[0] + (x - hinge[0]) * k, hinge[1] + (y - hinge[1]) * k]));
          const mx = pts.reduce((a, p) => a + p[0], 0) / pts.length;
          const lit = 1 + light * (1 - Math.min(1, Math.abs(mx - lx) / (cols * 0.45))) - light * 0.5;
          const v = Math.round(Math.min(1, f.shade * lit) * 255);
          sctx.fillStyle = `rgb(${v},${v},${v})`;
          sctx.beginPath();
          sctx.moveTo(pts[0][0], pts[0][1]);
          for (const p of pts.slice(1)) sctx.lineTo(p[0], p[1]);
          sctx.closePath();
          sctx.fill();
        });

        // 2. keep a reading area quiet
        if (fade) {
          const g = sctx.createRadialGradient(0, 0, 0, 0, 0, 1);
          g.addColorStop(0, "rgba(0,0,0,1)");
          g.addColorStop(0.75, "rgba(0,0,0,0.85)");
          g.addColorStop(1, "rgba(0,0,0,0)");
          sctx.save();
          sctx.translate(cols * fade.x, rows * fade.y);
          sctx.scale(cols * fade.rx, rows * fade.ry);
          sctx.fillStyle = g;
          sctx.beginPath();
          sctx.arc(0, 0, 1, 0, Math.PI * 2);
          sctx.fill();
          sctx.restore();
        }

        // 3. print: Bayer threshold, one square dot per lit cell, in this creature's ink
        const px = sctx.getImageData(0, 0, cols, rows).data;
        const path = new Path2D();
        for (let y = 0; y < rows; y++) {
          const by = BAYER[y & 7];
          for (let x = 0; x < cols; x++) {
            if (px[(y * cols + x) * 4] / 255 > by[x & 7]) path.rect(x * step, y * step, dot, dot);
          }
        }
        octx.fillStyle = c.ink;
        octx.fill(path);
      });

      if (!reduced) frame = requestAnimationFrame(draw);
    };

    // paint the first frame now, so the art never waits on the frame clock to appear
    if (visible || reduced) draw(performance.now());
    return () => cancelAnimationFrame(frame);
  }, [visible, creatures, cell, light, fade]);

  return (
    <div ref={host} className={`dither-origami${className ? ` ${className}` : ""}`} aria-hidden="true">
      <canvas ref={canvas} />
    </div>
  );
}
