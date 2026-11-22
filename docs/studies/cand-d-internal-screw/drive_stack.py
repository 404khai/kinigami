"""Exploratory Q98 sizing; no candidate I/O, no Gate evaluator. Units mm, N, N mm, g.

python3 drive_stack.py [--mass-g 46] [--mu-thread .20]
Changed mass affects only external loads, NOT the imported 46 g mechanics model.
"""
from argparse import ArgumentParser
from itertools import product
from math import atan, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan


def main():
    ap = ArgumentParser(description=__doc__)
    ap.add_argument("--mass-g", type=float, default=46)
    ap.add_argument("--mu-thread", type=float, default=.20)
    args = ap.parse_args()
    assert args.mass_g > 0 and args.mu_thread >= 0
    # Finished/profile-gauged dimensions; not machine or vendor tolerances.
    S, ds, nut0, le = 3.56, .03, 28.69, 1.56
    thread0, thread1 = 28.61, 33.91
    emarg = min(nut0-.02-(thread0+.02),
                thread1-.02-(nut0+.02+le+.02+S+ds))
    gap = 34.17-(34.02+.02)
    cam = .425/tan(radians(11.8))+.135/tan(radians(35))+1.06
    print(f"Stroke min {S-ds:.3f}; worst segmented track {cam:.3f}; "
          f"debit another .08 for blends -> reserve {S-ds-cam-.08:.3f}")
    print(f"Full-thread edge margin {emarg:.3f}; engagement >= {le-.02:.3f}; "
          f"solid tip gap >= {gap:.3f}; min open radial room {.735+.415+.125-1.10:.3f}")
    assert S-ds >= 3.49 and emarg > 0 and S-ds >= cam+.08 and gap > 0
    # Nominal nose extension .80 only on metal; retain v6 body's exact extents.
    c = (10.8262, 0, 0)
    def box(x0,x1,y0,y1,z0,z1):
        return max(dist(c,q) for q in product((x0,x1),(y0,y1),(z0,z1)))
    def cyl(x0,x1,r):
        return hypot(max(abs(x0-c[0]),abs(x1-c[0])),hypot(.6,-4.6)+r)
    radii = dict(body=max(box(1.8,34.4,-12.7,12.7,-12,12),
                          box(34.4,35.6,-11.9,11.9,-11.2,11.2),
                          box(-9.4,-1.8,-12.7,12.7,-12,12),
                          box(-10.6,-9.4,-11.9,11.9,-11.2,11.2)),
                 neg_ear=box(35.6,37.2,-9.1,-3.9,-10.7,-6.9),
                 pos_ear=box(35.6,37.2,5.1,10.3,-2.3,1.5),
                 head=cyl(35.6,37.2,7),teeth=cyl(37.0,37.4,6.3),
                 tail=cyl(-13.8,-10.6,6.3),tip=cyl(-16.75,-13.45,1.1))
    print("Sphere radii:", {k:round(v,4) for k,v in radii.items()})
    print(f"Sphere diameter {2*max(radii.values()):.3f}; two pose shifts 50.8, 101.6")
    W = .00980665*args.mass_g
    print(f"At {args.mass_g:g}g: 4W={4*W:.3f}, W={W:.3f}, "
          f"2W*12.7={25.4*W:.3f}, M_bend=50.8W={50.8*W:.3f} vs {48*W:.3f}")
    p=.35; d=2.5-.64952*p
    lam=atan(p/(pi*d)); f=d/2*tan(lam+atan(args.mu_thread/cos(pi/6)))
    print(f"Screw lead angle {degrees(lam):.2f}; self-lock requires mu > "
          f"{tan(lam)*cos(pi/6):.4f}; T/F={f:.4f}; "
          f"37.85/f={37.85/f:.1f} N (equivalence only)")
    for T in (49.03,176.52,200):
        print(f"T {T:.2f}: thrust frictionless {2*pi*T/p:.0f} N, "
              f"mu_thread {args.mu_thread:g} -> {T/f:.0f} N without losses")
    for m in (.18,.20):
        r=9*m; b=3.0; alpha=radians(20); Ered=210000/(2*(1-.3**2))
        for T in (49.03,200):
            Ft=T/r; Fn=Ft/cos(alpha); Rred=r*sin(alpha)/2
            pin=2*Fn
            print(f"planet m{m:.2f} T{T:g}: Ft {Ft:.1f}; "
                  f"root {Ft/(b*m*.30):.0f} MPa; pitch Hertz "
                  f"{sqrt(Fn*Ered/(pi*Rred*b)):.0f} MPa; "
                  f"pin {pin:.1f}N, bend {32*pin*4.4/(4*pi*1.8**3):.0f} MPa")
    for L in (8,10):
        gamma=2*.20*6/L
        print(f"offset L{L}: gamma {gamma:.3f}; at 5 Nmm parasitic "
              f"eta >= {(37.85/(1-gamma)+5)/(1.5*49.03):.3f}")
    print("Baseline non-replaced = 45.541 - .081 - 8.508 - 2.081 = 34.871 g; "
          "11.129 g left at 46 g. No mass-cap claim.")


if __name__ == "__main__":
    main()
