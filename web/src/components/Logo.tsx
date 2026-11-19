/**
 * The mark: a square sheet on its corner with its crease pattern. Mountain folds are solid,
 * valley folds dashed, and one flap is folded over in blue.
 */
export function Logo({ className = "logo-mark" }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 64 64" aria-hidden="true">
      <rect x="2" y="2" width="60" height="60" rx="6" className="lg-sheet" />
      <path d="M32 9 55 32 32 55 9 32Z" className="lg-edge" />
      <path d="M32 9 32 55M9 32 55 32" className="lg-mountain" />
      <path d="M20.5 20.5 43.5 43.5M43.5 20.5 20.5 43.5" className="lg-valley" />
      <path d="M32 9 55 32 32 32Z" className="lg-flap" />
    </svg>
  );
}
