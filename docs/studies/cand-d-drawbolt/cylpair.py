"""Take 16: larger isotropic spheres, continuously convex K/C tracks.
Conditional active regular-surface LP; centre envelopes explicitly selected.
"""
from math import asin,pi,cos,sin,hypot,sqrt,radians,ceil,floor
from itertools import product
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cand-d-exact-pairs'))
from mixed import cert
X,Y,Z=np.eye(3); R=6.; B=2.; DK=3.50; DC=4.; MU=.23
P=10; STEP=pi/24; fmax=hypot(1,MU/cos(pi/P))

def group(i,k,s,band,wide,stage):
    phi=radians(90+120*i); r=Y*cos(phi)+Z*sin(phi); t=np.cross(X,r)
    rows=[]; rhs=[]
    # G is optional flat rear; on eject the rear pads themselves advance.
    for j in range(band[0],band[1]+1):
        a=j*STEP
        if k=='K':
            n=-cos(a)*X-sin(a)*r; u=t
            er=[-.06-DK*sin(a),3.97-DK*sin(a)] if wide else [-.35,.35]
            loc=product([DK*(1-cos(a))],er,[-.70,.70])
        elif k=='C':
            n=sin(a)*X+s*cos(a)*t; u=r
            loc=product([DC*sin(a)],[-.50,.50],[-s*(.03+DC*(1-cos(a)))])
        else:
            n=X; u=r
            loc=product([-.10,4.20] if stage=='exit' else [0.],[-.65,.65],[-.65,.65])
        v=np.cross(n,u); loc=list(loc)
        for l in range(P):
            f=n+MU/cos(pi/P)*(cos(2*pi*l/P)*u+sin(2*pi*l/P)*v)
            extra=np.zeros(3); drag=0.
            if k=='K':
                gb=MU*(1.645*abs(f@X)+2.19*abs(f@t)+1.72*abs(f@r))
                extra[i]=-f@r-gb;drag=max(0.,gb+f@r)
            for xx,rr,tt in loc:
                c=(1+rr/R)*r+xx/R*X+tt/R*t
                wr=np.r_[f,np.cross(c-B/R*n,f),extra]
                rows.append(wr);rhs.append(drag)
                if k=='K' and abs(j)<=1:
                    rows.append(np.r_[wr[:6],0,0,0]);rhs.append(drag)
    delta=2*sin(radians(.5)/2); h=STEP**2/8 if k!='G' else 0.
    ef=fmax*(delta+h)
    # Max radius of reference vectors by full travel, plus local error:
    # K: [R-3.6,R+~7.5], x<=3.5; C including conditional backside
    # at 180: t excursion 8.03, x<=4, r<=6.5. Bound by 2.6*R.
    # c'(a),c''(a) <= max(DK,DC)/R, so (c x f)'' <= (|c|+3D/R)|f|.
    # .14 mm centre allowance covers actual x/r/t and half-gap/form deviations
    # in addition to the explicit extrusion offsets. Uniform normal uncertainty.
    em=2.6*ef+fmax*(.14/R+3*DC/R*h)+(B*(delta+h)+.015)/R*MU/cos(pi/P)
    err=np.r_[np.full(3,ef),np.full(3,em),np.zeros(3)]
    if k=='K':err[6+i]=ef*(1+MU*sqrt(1.645**2+2.19**2+1.72**2))
    return np.array(rows),err,np.array(rhs)+(err[6+i] if k=='K' else 0.)

def run(args):
    wide=not args.guided; stage=args.stage
    if args.kind=='fault':mz=52.2
    else:mz=14.5
    w=.05*9.80665; F=4*w; S=w; tx=25.4*w; my=50.8*w
    if args.kind=='correction':
        F+=w;tx+=w*15.12;my+=w*25.97;mz+=w*hypot(50.8,25.4)
    elif stage=='exit':F+=w
    # Full external wrench transferred from the tail-ring centre to head
    # origin. Any one real active centre bounds ring translation (no tail
    # attitude assumption). Tighter declared fixture box is optional.
    mt=3. if args.guided else 18.
    mx=4.3 if args.guided else 10.5
    tr=mt*S; bend=mt*F+mx*S
    load=np.array([F,S,S,(tx+tr)/R,(my+bend)/R,(mz+bend)/R,*([args.g0]*3)])
    # Each C range covers every angle compatible with its own K range even
    # if another station has already left. At x near 0 include negative chi.
    # DK and DC nominal +/- .03, x datum difference incl actual G <=.18.
    # Allow negative beta to -90 if blade can bear on its wrong side.
    ks=[(-12,-5),(-5,1),(1,5),(5,8),(8,12)] if wide else [(-1,4),(4,8),(8,12)]
    states={}; letters=[]
    for i in range(3):
        G=group(i,'G',1,(0,0),wide,stage)
        for s in (-1,1):
            if stage=='exit':
                states[i,'E',s]=[G,group(i,'C',s,(-1,24),wide,stage)]
                continue
            for j,band in enumerate(ks):
                lo=min(abs(x*STEP) for x in range(band[0],band[1]+1))
                hi=max(abs(x*STEP) for x in band)
                a=(DK-.03)*(1-cos(lo))-.18;b=(DK+.03)*(1-cos(hi))+.18
                low=floor(asin(max(-1,a/(DC+.03) if a>=0 else a/(DC-.03)))/STEP)
                high=ceil(asin(min(1,b/(DC-.03)))/STEP)
                K=group(i,'K',s,band,wide,stage); C=group(i,'C',s,(low,high),wide,stage)
                states[i,j,s]=[K,C]
            states[i,'R',s]=[G,group(i,'C',s,(-1,1),wide,stage)]
            states[i,'C',s]=[group(i,'C',s,(-1,24),wide,stage)]
    letters=['E'] if stage=='exit' else list(range(len(ks)))+['R','C']
    mx=0.; missed=0; ncase=0; critical=None
    for cfg in product(letters,repeat=3):
        # Six stations have cyclic symmetry. Wrench box is not axisymmetric;
        # overbound both bending components before removing cyclic permutations
        # (not used here). No station force sharing.
        for ss in product((-1,1),repeat=3):
            ncase+=1; gg=sum((states[i,cfg[i],ss[i]] for i in range(3)),[])
            if args.focus=='drive':foci=['drive']
            elif args.focus=='push':foci=[list(range(0,len(gg),2))]
            elif args.focus=='sum':foci=[range(len(gg))]
            else:foci=[[j] for j in range(len(gg))]
            for f in foci:
                out=cert(gg,load,f)
                if out is None:missed+=1
                elif out[0]>mx:mx=out[0];critical=(cfg,ss)
            if missed and args.fast:
                print('first missing',cfg,ss,'NOT a force bound',flush=True);return
    print(args.kind,stage,args.focus,'wide',wide,'g0',args.g0,'modes',ncase,'missing',missed,
          'max of certified modes only',mx,'critical',critical,flush=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--kind',choices=['service','fault','correction'],default='service')
    ap.add_argument('--stage',choices=['edge','exit'],default='edge')
    ap.add_argument('--focus',choices=['single','drive','sum','push'],default='sum')
    ap.add_argument('--g0',type=float,default=.8)
    ap.add_argument('--guided',action='store_true')
    ap.add_argument('--fast',action='store_true')
    run(ap.parse_args())
