import type { ReactElement } from "react";
import { gearPoints, polyD } from "../lib/gears";

function Gear({ x, y, teeth, module, dur, reverse, spokes = 5, phase = 0 }: {
  x: number; y: number; teeth: number; module: number; dur: number; reverse?: boolean; spokes?: number; phase?: number;
}) {
  const pitch = (module * teeth) / 2;
  const hub = pitch * 0.22;
  const rim = pitch - module * 2.4;
  return (
    <g transform={`translate(${x} ${y}) rotate(${phase})`}>
      <g className="bp-spin" style={{ animationDuration: `${dur}s`, animationDirection: reverse ? "reverse" : "normal" }}>
        <path d={polyD(gearPoints(0, 0, teeth, pitch - module * 1.25, pitch + module, 0))} className="bp-stroke" />
        <circle r={pitch} className="bp-dash" />
        <circle r={rim} className="bp-stroke" />
        <circle r={hub} className="bp-stroke" />
        <circle r={hub * 0.45} className="bp-stroke" />
        {Array.from({ length: spokes }, (_, i) => {
          const a = (i / spokes) * Math.PI * 2;
          return <line key={i} x1={Math.cos(a) * hub} y1={Math.sin(a) * hub} x2={Math.cos(a) * rim} y2={Math.sin(a) * rim} className="bp-stroke" />;
        })}
      </g>
      <line x1={-pitch - 40} y1="0" x2={pitch + 40} y2="0" className="bp-center" />
      <line x1="0" y1={-pitch - 40} x2="0" y2={pitch + 40} className="bp-center" />
    </g>
  );
}

function Dim({ x1, y1, x2, y2, label }: { x1: number; y1: number; x2: number; y2: number; label: string }) {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const vertical = x1 === x2;
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2} className="bp-stroke" markerStart="url(#bp-arr)" markerEnd="url(#bp-arr)" />
      <text x={mx} y={my} className="bp-text" textAnchor="middle" dy={vertical ? 0 : -6} transform={vertical ? `rotate(-90 ${mx} ${my}) translate(0 -6)` : undefined}>
        {label}
      </text>
    </g>
  );
}

function Cross({ x, y }: { x: number; y: number }) {
  return (
    <g className="bp-stroke">
      <circle cx={x} cy={y} r="9" />
      <line x1={x - 16} y1={y} x2={x + 16} y2={y} />
      <line x1={x} y1={y - 16} x2={x} y2={y + 16} />
    </g>
  );
}

/** A square sheet's crease pattern: a grid of mountain folds crossed by valley diagonals. */
function Creases({ x, y, size, n = 4 }: { x: number; y: number; size: number; n?: number }) {
  const s = size / n;
  const lines: ReactElement[] = [];
  for (let i = 1; i < n; i++) {
    lines.push(<line key={`v${i}`} x1={x + i * s} y1={y} x2={x + i * s} y2={y + size} className="bp-stroke" />);
    lines.push(<line key={`h${i}`} x1={x} y1={y + i * s} x2={x + size} y2={y + i * s} className="bp-stroke" />);
  }
  for (let i = 0; i < n; i++)
    for (let j = 0; j < n; j++) {
      const flip = (i + j) % 2 === 0;
      const [ax, ay, bx, by] = flip ? [0, 0, s, s] : [s, 0, 0, s];
      lines.push(<line key={`d${i}-${j}`} x1={x + i * s + ax} y1={y + j * s + ay} x2={x + i * s + bx} y2={y + j * s + by} className="bp-valley" />);
    }
  return (
    <g>
      <rect x={x} y={y} width={size} height={size} className="bp-stroke" />
      {lines}
    </g>
  );
}

/** Fixed drafting-table backdrop: grid (CSS), meshing gears, a crease pattern, dimensions, registration marks. */
export function Blueprint() {
  // Module 12: 30 teeth (pitch r 180) meshes 14 teeth (pitch r 84) at centre distance 264.
  return (
    <div className="blueprint" aria-hidden="true">
      <svg viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice">
        <defs>
          <marker id="bp-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0 1 L9 5 L0 9" fill="none" stroke="currentColor" strokeWidth="1.2" />
          </marker>
        </defs>

        <Gear x={1460} y={170} teeth={30} module={12} dur={120} spokes={6} />
        <Gear x={1460 - 264 * Math.cos(0.5)} y={170 + 264 * Math.sin(0.5)} teeth={14} module={12} dur={56} reverse spokes={4} phase={6} />
        <circle cx="1460" cy="170" r="300" className="bp-dash" />
        <Dim x1={1280} y1={420} x2={1640} y2={420} label="Ø 360.00 PCD" />

        <Creases x={70} y={700} size={240} />
        <Dim x1={70} y1={970} x2={310} y2={970} label="SHEET · M / V" />

        <g className="bp-text">
          <text x="1180" y="40">DET. A — DRIVE TRAIN · SCALE 2:1</text>
          <text x="70" y="680">DET. B — CREASE PATTERN</text>
          <text x="1300" y="960">KINIGAMI / NOTES / SHEET 01 OF 01</text>
        </g>

        <line x1="0" y1="610" x2="1600" y2="610" className="bp-center" />
        <line x1="860" y1="0" x2="860" y2="1000" className="bp-center" />

        <Cross x={40} y={40} />
        <Cross x={1560} y={960} />
        <Cross x={1560} y={40} />
      </svg>
    </div>
  );
}
