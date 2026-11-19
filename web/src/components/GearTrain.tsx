import { gearPoints, meshChain, polyD, type MeshGear } from "../lib/gears";

const M = 6; // module
const SEC_PER_TOOTH = 0.6;

const GEARS = meshChain(M, { z: 28, cx: 180, cy: 176 }, [
  { z: 14, deg: -22 },
  { z: 20, deg: 38 },
  { z: 10, deg: -32 },
]);

function GearShape({ g, tone }: { g: MeshGear; tone?: "ink" | "accent" }) {
  const pitch = (M * g.z) / 2;
  const root = pitch - M * 1.25;
  const hub = Math.max(7, pitch * 0.22);
  const rim = root - M * 1.4;
  const spokes = g.z > 14 ? 5 : 0;
  return (
    <g
      className={`gt-gear ${tone ?? ""}`}
      style={{ transformOrigin: `${g.cx}px ${g.cy}px`, animationDuration: `${g.z * SEC_PER_TOOTH}s`, animationDirection: g.dir === 1 ? "normal" : "reverse" }}
    >
      <path d={polyD(gearPoints(g.cx, g.cy, g.z, root, pitch + M, g.phase))} className="gt-body" />
      <circle cx={g.cx} cy={g.cy} r={pitch} className="gt-pitch" />
      {spokes > 0 && <circle cx={g.cx} cy={g.cy} r={rim} className="gt-line" />}
      {Array.from({ length: spokes }, (_, i) => {
        const a = g.phase + (i / spokes) * Math.PI * 2;
        return <line key={i} x1={g.cx + Math.cos(a) * hub} y1={g.cy + Math.sin(a) * hub} x2={g.cx + Math.cos(a) * rim} y2={g.cy + Math.sin(a) * rim} className="gt-line" />;
      })}
      <circle cx={g.cx} cy={g.cy} r={hub} className="gt-hub" />
      <circle cx={g.cx} cy={g.cy} r={hub * 0.4} className="gt-axle" />
    </g>
  );
}

/** A meshing four-gear train drawn as a blueprint detail. Pure decoration: it explains nothing about a Kin. */
export function GearTrain() {
  const [a, , , d] = GEARS;
  return (
    <svg className="geartrain" viewBox="0 0 560 360" role="img" aria-label="An animated train of four meshing spur gears, drawn as a blueprint detail">
      <defs>
        <marker id="gt-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M0 1 L9 5 L0 9" fill="none" stroke="currentColor" strokeWidth="1.4" />
        </marker>
      </defs>
      {GEARS.map((g, i) => (
        <GearShape key={i} g={g} tone={i === 1 ? "accent" : i === 3 ? "ink" : undefined} />
      ))}
      <g className="gt-anno">
        <line x1={a.cx - (M * a.z) / 2} x2={a.cx + (M * a.z) / 2} y1="322" y2="322" markerStart="url(#gt-arr)" markerEnd="url(#gt-arr)" />
        <text x={a.cx} y="340" textAnchor="middle">PCD {M * a.z} · Z{a.z} · M{M}</text>
        <text x={d.cx} y={d.cy - 56} textAnchor="middle">Z{d.z} · {(a.z / d.z).toFixed(1)} : 1</text>
        <text x="16" y="24">DET. C — A TRAIN THAT STAYS MESHED</text>
      </g>
    </svg>
  );
}
