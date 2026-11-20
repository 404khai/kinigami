import { useId } from "react";
import { SHAPES, type ShapeKind } from "../lib/origami";

/**
 * Paper-cut origami: the same faceted shapes as the dither fields, drawn flat. Each facet
 * takes one tone of a single hue (lighter where it faces the light), creases are thin
 * paper-white lines, a hard offset shadow sits down-right, and a fine grain sits on top.
 * `diagram` adds the marks of an instruction sheet: a dashed valley fold and a fold arrow.
 */

const hex = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
function tone(base: string, shade: number) {
  // shade 1 → 30% toward white, shade 0.4 → 40% toward ink
  const [r, g, b] = hex(base);
  const t = (shade - 0.7) / 0.3;
  const to = t >= 0 ? [255, 255, 255] : [17, 16, 21];
  const k = t >= 0 ? t * 0.3 : -t * 0.4;
  return `rgb(${[r, g, b].map((v, i) => Math.round(v + (to[i] - v) * k)).join(",")})`;
}

export function PaperOrigami({
  kind,
  color,
  tilt = 0,
  flip = false,
  diagram = false,
  shadow = true,
  className,
  title,
}: {
  kind: ShapeKind;
  color: string;
  tilt?: number;
  flip?: boolean;
  diagram?: boolean;
  shadow?: boolean;
  className?: string;
  title?: string;
}) {
  const id = useId().replace(/:/g, "");
  const facets = SHAPES[kind];
  const pt = ([x, y]: [number, number]) => `${(flip ? -x : x).toFixed(3)},${y.toFixed(3)}`;
  const first = facets[facets.length - 1].pts;
  const [ax, ay] = first[0];
  const [bx, by] = first[1];
  return (
    <svg className={`paper-origami${className ? ` ${className}` : ""}`} viewBox="-1.35 -1.25 2.7 2.6" role={title ? "img" : undefined} aria-hidden={title ? undefined : true}>
      {title && <title>{title}</title>}
      <defs>
        <filter id={`grain-${id}`} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="2.4" numOctaves="2" seed="7" result="n" />
          <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.16 0" result="g" />
          <feComposite in="g" in2="SourceGraphic" operator="in" result="gc" />
          <feMerge>
            <feMergeNode in="SourceGraphic" />
            <feMergeNode in="gc" />
          </feMerge>
        </filter>
      </defs>
      <g transform={`rotate(${(tilt * 180) / Math.PI})`}>
        {shadow && (
          <g transform="translate(0.07 0.09)" className="po-shadow">
            {facets.map((f, i) => (
              <polygon key={i} points={f.pts.map((p) => pt(p as [number, number])).join(" ")} />
            ))}
          </g>
        )}
        <g filter={`url(#grain-${id})`}>
          {facets.map((f, i) => (
            <polygon key={i} points={f.pts.map((p) => pt(p as [number, number])).join(" ")} fill={tone(color, f.shade)} className="po-facet" />
          ))}
        </g>
        {diagram && (
          <g className="po-diagram">
            <line x1={flip ? -ax : ax} y1={ay} x2={flip ? -bx : bx} y2={by} />
            <path d={`M ${(flip ? -1 : 1) * (ax + 0.25)} ${ay - 0.35} q ${(flip ? -1 : 1) * 0.35} -0.05 0.2 0.3`} markerEnd={`url(#arrow-${id})`} />
          </g>
        )}
      </g>
      {diagram && (
        <defs>
          <marker id={`arrow-${id}`} viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M0 1 L9 5 L0 9 Z" />
          </marker>
        </defs>
      )}
    </svg>
  );
}
