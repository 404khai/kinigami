/**
 * The folding K. Three pieces of paper: a notched stem, an upper arm hinged on the stem's
 * right edge, and a lower arm hinged under it. On load (and on hover of `.brand`) each arm
 * unfolds from behind the stem: it starts mirrored over the stem showing the sheet's darker
 * back, passes edge-on, and lands showing its face.
 */
export function KLogo({ className = "klogo", title = "Kinigami" }: { className?: string; title?: string }) {
  return (
    <svg className={className} viewBox="0 0 64 64" role={title ? "img" : undefined} aria-hidden={title ? undefined : true}>
      {title && <title>{title}</title>}
      <polygon className="k-stem" points="9,8 27,8 27,56 9,56 9,38 14,32 9,26" />
      <line className="k-crease" x1="27" y1="8" x2="27" y2="56" />
      <g className="k-arm k-arm-up">
        <polygon className="k-face" points="27,8 56,8 34,31 27,31" />
      </g>
      <g className="k-arm k-arm-down">
        <polygon className="k-face" points="27,31 36,31 56,51 56,56 41,56 27,42" />
      </g>
    </svg>
  );
}
