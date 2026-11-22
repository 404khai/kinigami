"""Take 68: rigid buttons and three sprung head-side saddles. Exploratory, N/mm."""
from itertools import product
from math import acos, cos, hypot, pi, radians, sin, sqrt, tan
import numpy as np
from fixed_face import A, BACK, BC, CLOCK, CX, DELTA, HOME, MU, POS, RAD, RIM, X, Y, Z, loads, reactions, setup
from edge_hertz import hertz
from tail_buttons import bound

ANG, Q, MID = 56., .60, 28.
C,S=cos(radians(ANG)),sin(radians(ANG))


def saddle():
    pole_t=BACK*S; pole_x=BC-BACK*C
    ht=pole_x-HOME; k=tan(radians(ANG))
    cap=-5.30
    # The moving island extends behind its crown: clip entire pyramid to a
    # radial cone, not a vertical cut through its working land.
    radial_cap, halfwidth, outer=11.88,1.35,3.81
    slope_margin=min(ht/S,(cap-pole_x)/S,
        (k*halfwidth-ht)/hypot(k,S),(k*(outer-pole_t)-ht)/(2*S))
    # In-plane radial distance is 1-Lipschitz, h changes by <= sin(a) per
    # unit in-slope displacement. Gives a safe distance to the conical trim.
    cone_margin=(radial_cap-hypot(RAD,pole_t)-ht/k)/(1+S/k)
    top_t=pole_t+(cap-pole_x)/k; top_outer=outer-(cap-HOME)/k
    top_half=halfwidth-(cap-HOME)/k
    top_rad=hypot(RAD,top_t)
    print('pole x,t / top length, halfwidth / polygon,cap-circle pole margins / top trim reserve at inner crest',np.round(
        [pole_x,pole_t,top_outer-top_t,top_half,slope_margin,cone_margin,radial_cap-(cap-HOME)/k-top_rad],4))
    assert min(top_outer-top_t,top_half,cone_margin,radial_cap-(cap-HOME)/k-top_rad)>0
    land=min(slope_margin,cone_margin)
    # Socket-facing capsule slope. Own working normal passes through ball
    # centre. No reliance on a fragile straight shaft or an open ball port.
    dx,dr=0.-BC,5.-RAD
    print('added capsule centreline length / own V support plane gain / projection on nearest jaw radial axis incl R',
          np.round([hypot(dx,dr),C*dx,.5*RAD+BACK],4))
    # Maximum radial coordinate of pocket opening is 11.94. Curved clipping
    # leaves a complete circular land around all three openings.
    depth,wall_slope=.91,.55/1.6
    rin=radial_cap+.06
    print('front annulus / minimum remaining radial ligament at blind-pocket depth / rear bed / pad engagement / bed stop clearance',
          np.round([A-rin,A-depth*wall_slope-rin,1.60-depth,.62-.21,depth-(.62+.22)],4))
    assert A-depth*wall_slope>rin
    # Every point of the nominal face projection has metal at or above
    # -u within h transversely. This uses a constant-width Euclidean
    # offset of a convex island (not two box face offsets at corners).
    R,H,dn,up=2.45,.085,.24,.23
    nx=(sqrt(R*R-H*H)-dn-up)/R
    work=lambda n: cos(acos(n)+DELTA)-MU*sin(acos(n)+DELTA)
    gap=14.54-A+.05; tr=sqrt(R*R-gap*gap)
    rim=min(tr/R,1-1.45/R)
    print('plate skirt nx / axial work per N skirt,56deg facet,annular edge / terminal outer rim lift',np.round(
        [nx,work(nx),work(C),work(rim),1.35-(R-tr)],5))
    # Inside an opening this weaker (not radius-at-rim) terminal case suffices.
    print('terminal lift for inward projection even at full seat recession',
          round(1.35-dn+sqrt(R*R-H*H)-R,5))
    return land


def supports(land):
    req=[bound(Q,60.,.10,c,angle=ANG) for c in ('service','table','fault')]
    print('required nominal axial preload three cases',np.round(req,4))
    print('trial maximum mass (g) for this sufficient seated bound at S=28 / table S at 74.32 and 120 g',
          np.round([70*MID/req[1],req[1]*74.32/70,req[1]*120/70],4))
    assert max(req)<MID
    for k in (0.,.02,.05,.12,.23,.32):
        est=reactions(guide=k,lo=.9*MID,hi=1.1*MID,angle=ANG,qx=Q,phase=60,tail_springs=True)
        f,j=est.max(axis=0)
        print('guide coefficient / seat,jaw reaction estimates / Hertz a,p GPa / edge reserve',k,end=' ')
        if np.isfinite(f):
            a,_,p=hertz(f,BACK,BACK)
            print(np.round([f,j,a,p/1000,land-POS-a],4))
        else: print('no bound')
    # The spring is at the moving saddle and is pushed backwards on contact;
    # it does not close a leaf. Equivalent to relative button motion in the
    # nine-contact normal-only virtual balance, but *not* in guide loading.
    D,d,active,turns,G=3.7,.72,4.,6.,79300.
    k=G*d**4/(8*D**3*active); Cc=D/d;wahl=(4*Cc-1)/(4*Cc-4)+.615/Cc
    ext,comp=.21,.22
    print('trial coil stiffness / free length / solid margin at inward stop / loaded stress MPa',np.round(
        [k,5.12+MID/k,5.12-comp-turns*d,wahl*8*(MID+k*comp)*D/(pi*d**3)],4))
    # A common draw cannot fix differential button offset. For total variation
    # in indicated compression, calibration and preload scatter add separately.
    print('matched spring max axial half-error for 10% band, if residual spring errors are 0 /.7 /1.5 N',
          np.round([(MID*.10-err)/k for err in (0.,.7,1.5)],4))


def guides():
    p,n,J=setup(RAD,radians(ANG),radians(CLOCK))
    A9=np.zeros((9,9));A9[:6,:6]=J
    for j in range(3):
        t=radians(CLOCK+60+120*j);r=cos(t)*Y+sin(t)*Z
        q=Q*X+sqrt(1-Q*Q)*r;pt=(CX+BACK*Q-BC)*X+(RIM+BACK*sqrt(1-Q*Q))*r
        A9[:6,6+j]=-np.r_[q,np.cross(pt,q)/RAD]
        A9[6+j,2*j:2*j+2]=C
    B=np.array([np.r_[loads('table')*sg[:6],MID*(1+.1*np.array(sg[6:]))]
                for sg in product((-1,1),repeat=9)])
    N=np.linalg.solve(A9,B.T).T
    assert N.min()>0 and np.max(abs(N@A9.T-B))<1e-10
    print('clean table corners minimum virtual normal; here also a real frictionless equilibrium (N)',round(N.min(),4))
    # Infinitesimal contact-offset tolerance, not a finite registration proof.
    # A9.T maps body and three saddle motions to signed normal gap changes.
    H=np.linalg.inv(A9.T)
    motion=np.max(np.sum(abs(H[6:]),axis=1))
    diff=max(np.sum(abs(H[j]-H[k])) for j,k in ((6,7),(7,8),(8,6)))
    print('nominal differential saddle sensitivity: absolute and pairwise per mm of independent normal-gap errors',
          np.round([motion,diff],5))
    # The force acts through the sphere centre; coil and guide loads on the
    # saddle—not on the tail—are needed. Coil has no moment about station radial
    # axis as long as it is on the same meridian. Radial axis is perpendicular
    # to guide travel (not the rail's longitudinal roll rating).
    for length,Mr in ((11.9,.4),(16.1,1.1)):
        xg=-7.75-length/2
        ft=np.abs(N[:,::2][:,:3]-N[:,1:6:2])*S
        M=ft*abs(BC-xg)*.001
        print('carriage L / projected M max Nm / smooth guide recommendation .1 to .3 M0',np.round(
            [length,M.max(),.1*Mr,.3*Mr],4))
    # Attempt A: short commercial rail, backed by a full bracket on a post.
    # A local AABB is actual bracket material, not a hollow guide reservation.
    # Radial cylinder shell of the old drum: R9.78..13.19 with a disk track
    # cut from the inner wall. Use BOTH x AND radius outside the cutter
    # before calling a result a material overlap.
    # A separate simpler witness: old post occupies x[-19.72,-8.43],
    # r[8.15,9.49], t[-1.48,1.48] on THIS seat meridian. New back bracket
    # caps that post-overlapping space while attached to the moving saddle.
    block=[(-18.8,-8.8),(8.07,8.55),(-1.25,1.25)]
    post=[(-19.72,-8.43),(8.15,9.49),(-1.48,1.48)]
    intersection=[(max(a,c),min(b,d)) for (a,b),(c,d) in zip(block,post)]
    rad=min(hi-lo for lo,hi in intersection)/2
    print('separate saddle bracket in previous disk post: common ball centre in local x,r,t / radius',
          np.round([(lo+hi)/2 for lo,hi in intersection]+[rad],4))
    assert rad>0
    # Alternate roll of the complete back cassette inboard: examine the
    # R of the yoke vs the circular opening at the home front register.
    print('attempt A guide reservation corner r / old drum ID / rail required axial rear x',
          np.round([hypot(8.50,4.),9.78,-7.75-20.],4))


if __name__=='__main__':
    supports(saddle())
    guides()
