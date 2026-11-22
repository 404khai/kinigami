"""Take 12. Nominal closed-to-open section and tolerance screens; no candidate I/O.
mm, N, N mm, degrees. Optional --csv lists the complete coupled sweep.
"""
import argparse
import csv
from itertools import product
from math import cos, dist, hypot, pi, radians, sin, sqrt

R, B = 4.65, 1.05
HEAD, BALL_X, STOP, BLADE = 36.9, 34.65, 33.60, 35.85
CHEEK, LIP, THROW, LIFT, PIN = 34.96, 4.31, 1.65, 1.80, 2.30
# Station-local (radial, tangential) axes; a crown at +z avoids a bottom lobe.
AZ = (90,210,330)


def ramp(q,a,b,e,d):
    """Constant-speed middle and quadratic endpoint blends. Returns mm, mm/rad."""
    v=d/(b-a-e)
    if q<=a: return 0.,0.
    if q>=b: return d,0.
    u=q-a
    if u<e: return .5*v*u*u/e, v*u/e*180/pi
    if q>b-e: return d-.5*v*(b-q)**2/e,v*(b-q)/e*180/pi
    return v*(u-e/2),v*180/pi


def pose(q):
    r,k=ramp(q,12,108,8,THROW)
    x,h=ramp(q,112,156,5,LIFT)
    return r,k,x,h


def yz(r,t,az):
    a=radians(az)
    return .60+r*cos(a)-t*sin(a),-4.60+r*sin(a)+t*cos(a)


def jaw_curve(q,clock):
    a=radians(clock-q)
    r=PIN+pose(q)[0]
    return r*cos(a),r*sin(a)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv",metavar="path")
    p.add_argument("--mu",type=float,default=.23)
    a=p.parse_args()
    assert 0<=a.mu<.4
    qseq=[i/10 for i in range(1621)]
    # Centre paths thickened by slot widths; the global min needn't be at equal angle.
    A=[jaw_curve(q,0) for q in qseq]; C=[jaw_curve(q,120) for q in qseq]
    d=sqrt(min((u-y)**2+(v-z)**2 for u,v in A for y,z in C))
    # Lipschitz: arc+radial speed <4.2 mm/rad, two half-sample steps.
    web=d-.82-4.2*radians(.1)
    # Two 180deg-separated axial tracks; nonperiodic individual cam sectors, reversible.
    print(f"Planar slot to slot min centre {d:.3f}; web >= {web:.3f} after .82 width and sampling")
    assert web>.12
    # Bounds are deliberate gauge calls, including location/form, not vendor tolerances.
    print(f"axial pocket gap min {35.83-33.62-2.12:.3f}, max {35.87-33.58-2.08:.3f}")
    open_gap=LIP-.025+THROW-.025-(R+.035+1.06+.06)
    out_gap=STOP-.02+LIFT-.035-.14-(CHEEK+.025)
    neck_gap=1.60-(.50+.08)
    print(f"open sphere radial gap {open_gap:.3f}, rear-ball/cheek gap after eject {out_gap:.3f}, "
          f"fork/neck lateral gap {neck_gap:.3f}")
    assert min(open_gap,out_gap,neck_gap)>0
    max_r=max(hypot(r,t) for r,t in product((1.80,6.80),(-2.12,2.12)))
    body_r=29.6782
    nose_r=max(dist((10.8262,0,0),(x,*yz(r,t,az))) for az in AZ
               for x,r,t in product((35.60,HEAD),(1.80,7.55),(-2.18,2.18)))
    print(f"max fork local radius {max_r:.3f}, front frame witness R={nose_r:.3f}, "
          f"head/body diameter <= {2*max(body_r,nose_r):.3f} (listed pieces)")
    mu=a.mu
    worst=(0.,0.)
    for q in qseq:
        s,k,x,h=pose(q)
        r=PIN+s
        G=(k+mu*r)/(1-mu*k/r) if k else 0.
        # Finite shoulder friction charged in base F0; additional pin side load and
        # longitudinal offset of radial actuation -> one-sided guide friction.
        gamma=mu*G/r+2*mu*3.02/3.70
        if k: worst=max(worst,(G/(1-gamma) if gamma<1 else float("inf"),q))
    fac,q=worst
    print(f"mu={mu:.2f} radial worst T/F0={fac:.3f} at {q:.1f}deg; at 3 Nmm other "
          f"losses F0 limit {(49.03-3)/fac:.2f}; T at F0=10,17: "
          f"{3+10*fac:.2f}, {3+17*fac:.2f}")
    k=ramp(135,112,156,5,LIFT)[1]; re=5.38; emax=R+re; span=6.60
    G=(k+mu*re)/(1-mu*k/re)
    gamma=2*mu*emax/span+mu*G/re
    print(f"Eject, one follower & opposite pad: G={G:.3f}, gamma={gamma:.3f}, "
          f"remaining load budget {max(0,(49.03-3)*(1-gamma)/G):.2f} N")
    if a.csv:
        with open(a.csv,"w",newline="") as f:
            w=csv.writer(f)
            w.writerow(("deg","lip_r","pin_r","eject_x","ball_cent_x","exit_gap","track_drdtheta","track_dxdtheta"))
            for q in qseq:
                s,k,x,h=pose(q)
                w.writerow((q,LIP+s,PIN+s,STOP+x,BALL_X+x,STOP+x-CHEEK,k,h))


if __name__=="__main__":
    main()
