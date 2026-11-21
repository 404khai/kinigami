"""Take 21 analytical handoff coupon. N, mm, kPa; not a physical validation."""
from itertools import product
from math import atan,asin,sqrt,cos,sin,hypot,pi,radians,degrees
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cand-d-central-grasp"))
import seats

def out(l,*xs): print(l, *(round(x,6) for x in xs))
def need(S,M):
    return max(seats.need_pull(S,M,k) for k in ('service','table','fault'))
old=seats.R
W=seats.W
loads=np.r_[4*W,W,W,25.4*W/old,50.8*W/old,52.2/old]
out('old R6.30 nominal fault box necessary pull, ideal low-axis disk max',
    max(np.abs(d)@loads/d[0] for d in seats.H.T),.101325*pi*7.4**2)
seats.R=9.25;seats.W=.060*9.80665
R=seats.R; W=seats.W
ri,ro,d=5.90,12.75,.050
A0=pi*(ro**2-ri**2);Al=pi*((ro-d)**2-(ri+d)**2);Ah=pi*((ro+d)**2-(ri-d)**2)
th=radians(1.15)
# Opposite half-circles at their extreme radial boundary displacements.
e_ring=2*sum((r+d)**3-(r-d)**3 for r in [ri,ro])/(3*Al)
# Arbitrarily signed nonuniform axial gauge field <= .50 kPa about its mean.
m_field=.0005*4*((ro+d)**3-(ri-d)**3)/3
out('effective area min,nom,max; centroid radial error, pressure field moment',
    Al,A0,Ah,e_ring,m_field)
out('nominal 85kPa thrust; raised draw demand S=2 M=10 service/table/fault',
    .085*A0,*[seats.need_pull(2,10,k) for k in ('service','table','fault')])

def window(f,i,closed=False):
    # Vacuum at f / draw remaining at i. Includes tolerance on both actual
    # OUTPUT forces. Seated vacuum area excludes no isolated islands.
    Vmin=max(0,85*f-.50)*Al*.001*cos(th) if f else 0.
    Vmax=(85*f+.50)*Ah*.001 if f else 0.
    nominal=35*(1-i)
    drift=(.40+24*.04) if closed else .40
    Pmin=max(0,nominal-drift)
    Pmax=nominal+drift if nominal else 0.
    # Trial measured worst parasitics. P is actual fork axial draw.
    link=(.060*Pmax+2*.30)/7
    Sbar=link+.20
    Mbar=11.5*link+.025*Pmax+.30+.70
    # .20 N and .40 Nmm extra for nonplanar local pressure disturbance;
    # seal compression, side load and MOMENT are independent gauge tests.
    S=Sbar+Vmax*sin(th)+.20+.20
    M=Mbar+Vmax*(e_ring+.035+1.0*sin(th))+m_field*bool(f)+.40+1.50
    # Worst seal opening reaction at actual seated pose. Lower bound on
    # draw must subtract it. Do not subtract it when bounding max preload.
    lower=Pmin+Vmin-1.00; upper=Pmax+Vmax
    return lower,upper,S,M,need(S,M),Pmin,Pmax,Sbar,Mbar

N=12
stages=[(i/N,i/N) for i in range(N+1)]+[((i+1)/N,i/N) for i in range(N)]
rows=[window(*q) for q in stages]+[window(0,0,closed=True)]
out('handoff min net, max gross, max S, max M, minimum net minus own case demand',
    min(r[0] for r in rows),max(r[1] for r in rows),max(r[2] for r in rows),
    max(r[3] for r in rows),min(r[0]-r[4] for r in rows))
for name,ff,ii,isclosed in [('locked thermal',0,0,True),('both first step',1/N,0,False),
                            ('vacuum, fork clear',1,1,False)]:
    lo,hi,S,M,need_,*_=window(ff,ii,isclosed)
    out(name+' net min, gross max, S, M, required, reserve',lo,hi,S,M,need_,lo-need_)
assert min(r[0]-r[4] for r in rows)>0.
rect=min(window(j/N,j/N)[0]-window((i+1)/N,i/N)[4]
         for i in range(N) for j in (i,i+1))
out('continuous pump/draw substep rectangle reserve N',rect)
assert rect>1.67
lo,hi,ss,mm,_,*_=window(1,1)
out('vacuum-only reserve with separate blocked tool envelope (.35 axial,.30 side,1.5 couple)',
    lo-.35-need(ss+.30,mm+1.50))
_,_,_,_,req,_,_,_,_=window(0,0,closed=True)
out('closed maximum lost displacement at k=24 and .40 gauge, before other losses',
    (35-.40-1.00-req)/24)
G=max(r[1] for r in rows)
kx=cos(radians(45.5))-.23*sin(radians(45.5))
out('all-face sum normal ceiling; wrong full overlap gross and sum ceiling',
    (G+5*W)/kx,35.4+.0855*Ah,(35.4+.0855*Ah+5*W)/kx)

# Original ball/fork, distinct branch. Cylinder axes parallel to slide u.
Bhi,Blo=3.215,3.185
rrlo,rrhi=.435,.465
Tc=1.95; err=.025+.200; cmin,cmax=Tc-err,Tc+err
Xmin,Xmax=3.35,3.45
theta=asin(cmax/(Blo+rrlo)); qx=cos(theta)-.23*sin(theta)
out('original fork transverse neck reserve / sphere clearance / max backed normal',
    cmin-rrhi-(1.02+4.6*sin(th)),hypot(Xmin,cmin)-(Bhi+rrhi),36.36/qx)
out('original: min flange-to-nose over 7.5 radius, minimum slide for u-tip=2',
    4.30-7.5*sin(th)/cos(th)-Xmax-rrhi,2+.20+Bhi+.15)

# Inverted T occupies a blind tail recess. Values relative to passive face.
b,t=2.55,.55; yaw=radians(2.); dxy=.16; dztilt=.04
out('aligned long/short entry clearances',
    2.90-(b+t*sin(yaw)+dxy+dztilt),.95-(t+b*sin(yaw)+dxy+dztilt))
out('rotation bore / stem / back-plane / floor clearance',
    2.98-(hypot(b,t)+dxy+dztilt),1.16-(.78+dxy+dztilt),
    1.83-1.65,3.10-2.90)
out('minimum bar withdrawal stroke to hide behind head front (no gap credit)',
    2.90+.20+.05)
out('floor radial envelope clearance at z+1 before outer lip stock',13.-(ro+d))

P=36.36;rb=2.;Q=asin(2.50/7.90)+radians(1.65)
cx=cos(Q)-.23*sin(Q)
Fn=P/cx; lateral=(sin(Q)+.23)*Fn
S=(.06*P+.6)/7+.20
M=11.5*((.06*P+.6)/7)+.025*P+.30+.70
diff=(M+.16*P+3.*S+.15*lateral)/rb
Aplus=(P+diff)/2;Aminus=(P-diff)/2
Ri=1/(1/1.95-1/8.10)
nf=Aplus/cx
patch=(3*nf*Ri/(4*115400))**(1/3)
out('T chord: off-axis point force moment, radial F all feet, min axial/normal',
    rb*P,lateral,cx)
out('closed imbalance axial bound, min EACH axial, max one normal, Hertz p0 GPa, patch',
    diff,Aminus,nf,3*nf/(2*pi*patch*patch)/1000,patch)
out('uncertified rigid drive: possible T roll friction torque alone',.23*2.50*Fn)
out('0.15 mm seat height mismatch over 3.68 mm, pitch deg',degrees(atan(.15/3.68)))
out('locked minimum each axial over 33.64..36.36', (33.64-diff)/2)
# Unpowered yaw guard: ONE engaged flank of a single tail-side clocking key,
# no axial bottom. No independent assumed bound on its reaction.
kN=cos(radians(1))-.23*sin(radians(1))
kA=sin(radians(1))+.23
rk=2.25*kN-.15*kA  # min effective roll arm incl off-axis friction
tau=.23*2.50+.20*sin(Q)+2.50*2*sin(radians(.5))
Nf=(P+kA*M/rk)/(cx-kA*tau/rk);Nk=(M+tau*Nf)/rk
dA=(M+.16*(P+kA*Nk)+3*S+.15*(sin(Q)+.23)*Nf+
    .40*hypot(1,.23)*Nk+2.55*kA*Nk)/rb
single=(P+kA*Nk+dA)/(2*cx)
pa=(3*single*Ri/(4*115400))**(1/3)
out('side key active: sum foot normals, key N, min each foot axial across window',
    Nf,Nk,(33.64-kA*Nk-dA)/2)
out('side key active: one foot normal, p0 GPa, patch',single,3*single/(2*pi*pa**2)/1000,pa)
# Quantified hold-up is for a bounded leak only; gross de-seal unbounded.
drop=rect/(.001*Ah)
out('step reserve as pressure fall kPa; min cm3 for .020 std cm3/s x 2s at 101.325kPa',
    drop,101.325*.020*2/drop)
out('vented required delivered push, <=1 kPa cavity and .75 N measured adhesion',
    5*W+.001*Ah+.75)
# Jam when vacuum fails during angular overlap loss: a pure tension 4W.
out('seal loss: unsupported pure axial load once aperture aligned',4*W)
