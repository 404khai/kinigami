import { useEffect, useRef, useState } from "react";

/**
 * The folding K. Three pieces of paper: a notched stem, an upper arm hinged on the stem's
 * right edge, and a lower arm hinged under it. On load each arm unfolds from behind the
 * stem (CSS). The same three pieces refold into a crane: the stem becomes body and tail, the
 * upper arm the raised wing, the lower arm the neck and head. Each piece keeps its vertex
 * count, so the fold is a straight interpolation, staggered wing → neck → body.
 */

type Poly = [number, number][];
type Piece = { k: Poly; crane: Poly; kFill: string; craneFill: string; span: [number, number] };

export const PIECES: Record<"stem" | "up" | "down", Piece> = {
  stem: {
    k: [[9, 8], [27, 8], [27, 56], [9, 56], [9, 38], [14, 32], [9, 26]],
    crane: [[5, 13], [24, 37], [32, 35], [44, 40], [32, 51], [19, 43], [9, 25]],
    kFill: "#5b3df5",
    craneFill: "#5b3df5",
    span: [0.35, 1],
  },
  up: {
    k: [[27, 8], [56, 8], [34, 31], [27, 31]],
    crane: [[23, 38], [25, 3], [37, 20], [41, 38]],
    kFill: "#5b3df5",
    craneFill: "#8f7bff",
    span: [0, 0.65],
  },
  down: {
    k: [[27, 31], [36, 31], [56, 51], [56, 56], [41, 56], [27, 42]],
    crane: [[37, 39], [52, 12], [57, 8], [62, 18], [56, 15], [46, 41]],
    kFill: "#5b3df5",
    craneFill: "#24157a",
    span: [0.2, 0.85],
  },
};

const ease = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const hex = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const mixHex = (a: string, b: string, t: number) => {
  const [x, y] = [hex(a), hex(b)];
  return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * t)).join(",")})`;
};

/** A piece at fold progress p (0 = K, 1 = crane). */
export function pieceAt(piece: Piece, p: number) {
  const t = ease(Math.min(1, Math.max(0, (p - piece.span[0]) / (piece.span[1] - piece.span[0]))));
  const points = piece.k.map(([x, y], i) => `${(x + (piece.crane[i][0] - x) * t).toFixed(2)},${(y + (piece.crane[i][1] - y) * t).toFixed(2)}`).join(" ");
  return { points, fill: mixHex(piece.kFill, piece.craneFill, t), t };
}

/** Animate a number toward a target with requestAnimationFrame. */
function useTween(target: number, ms = 900) {
  const [v, setV] = useState(target);
  const from = useRef(target);
  useEffect(() => {
    const start = performance.now();
    const a = from.current;
    if (a === target) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
      from.current = target;
      setV(target);
      return;
    }
    let raf = 0;
    const step = (now: number) => {
      const k = Math.min(1, (now - start) / (ms * Math.abs(target - a)));
      const next = a + (target - a) * k;
      from.current = next;
      setV(next);
      if (k < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [target, ms]);
  return v;
}

export function KLogo({
  className = "klogo",
  title = "Kinigami",
  fold,
  tone = "violet",
}: {
  className?: string;
  title?: string;
  /** drive the fold yourself (0 = K, 1 = crane); omitted, it folds while the brand link is hovered */
  fold?: number;
  /** "paper" draws the mark in paper white, for violet or ink grounds */
  tone?: "violet" | "paper";
}) {
  const svg = useRef<SVGSVGElement>(null);
  const [hover, setHover] = useState(false);
  const tweened = useTween(hover ? 1 : 0);
  const p = fold ?? tweened;

  useEffect(() => {
    if (fold !== undefined) return;
    const host = svg.current?.closest(".brand, .wordmark");
    if (!host) return;
    const on = () => setHover(true);
    const off = () => setHover(false);
    host.addEventListener("pointerenter", on);
    host.addEventListener("pointerleave", off);
    return () => {
      host.removeEventListener("pointerenter", on);
      host.removeEventListener("pointerleave", off);
    };
  }, [fold]);

  const stem = pieceAt(PIECES.stem, p);
  const up = pieceAt(PIECES.up, p);
  const down = pieceAt(PIECES.down, p);
  const paper = tone === "paper";
  const fill = (f: string, alpha: number) => (paper ? `rgba(244,242,255,${alpha})` : f);
  return (
    <svg ref={svg} className={`${className}${paper ? " klogo-paper" : ""}`} viewBox="0 0 64 64" role={title ? "img" : undefined} aria-hidden={title ? undefined : true}>
      {title && <title>{title}</title>}
      <polygon points={stem.points} style={{ fill: fill(stem.fill, 1) }} />
      <line className="k-crease" x1="27" y1="8" x2="27" y2="56" style={{ opacity: 0.6 * (1 - stem.t) }} />
      <g className="k-arm k-arm-up">
        <polygon className="k-face" points={up.points} style={{ fill: fill(up.fill, 1 - 0.18 * up.t) }} />
      </g>
      <g className="k-arm k-arm-down">
        <polygon className="k-face" points={down.points} style={{ fill: fill(down.fill, 1 - 0.34 * down.t) }} />
      </g>
    </svg>
  );
}
