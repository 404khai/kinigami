"""Actual two-band force equilibrium and enclosing finite-interface wrench LP."""
from geo83 import *
from itertools import product
from scipy.optimize import linprog
def wrench(q,f):return np.r_[f,np.cross(q,f)]
def rays(n,outer=False,K=12):
    l=np.cross(n,np.eye(3)[np.argmin(abs(n))]);l/=np.linalg.norm(l)
    return [n+mu/(cos(pi/K) if outer else 1)*(l*cos(a)+np.cross(n,l)*sin(a)) for a in np.arange(K)*2*pi/K]
def inside(reset=0.,alpha=0.,peak_index=None):
    data={};a0=rad(alpha);dg=toe*(1-cos(a0)); qtop=1.5*(-sin(a0)*X+cos(a0)*Y); top_f=-qtop/1.5-mu*(cos(a0)*X+sin(a0)*Y)
    # Actual roller lies against the forward (+x) walls. Aligned journal contact
    # extends across cheek thickness. In this realization endcaps have free play.
    for direction in list(np.c_[np.zeros(72),np.cos(np.arange(72)*pi/36),np.sin(np.arange(72)*pi/36)])+[0*Z]:
        off=.05*direction;d=off+(.0015+reset+dg)*X; cols=[];ids=[];P=[];C=[]
        def add(k,tail=None,roll=None,i=0,sl=None,p=0,c=0):
            v=np.zeros(30)
            if tail is not None:v[:6]=tail
            if roll is not None:v[6+i*6:12+i*6]=roll
            if sl is not None:v[-6:]=sl
            cols.append(v);ids.append(k);P.append(p);C.append(c)
        pts,ns,cs=contacts()
        gaps=ns[:6]@d
        if min(gaps)<-.045 or sum(gaps<-.025)>1:continue
        for j in range(6):
            if gaps[j]>.025:continue
            assert gaps[j]>=-.045
            for f in rays(ns[j]):add('V'+str(j),tail=wrench(pts[j],f))
        for j,a in enumerate(np.radians([0,120,240])):
            B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T
            cen=B@np.array([-4.22+d[0]-dg,r0+dg+off@B[:,1],off@B[:,2]])
            # Crowns: nominal sticking pressure resultants at center, not generator endpoints.
            # Axle has no spin on this incipient branch; true EHL/traction not implied.
            for k,m,qs in [('tail',(X+Y)*c45,[-1.50*(X+Y)*c45]),('sleeve',-qtop/1.5,[qtop]),
                           ('wall',-X,[.50*X+t*Z for t in [-3.20,-2.99,2.99,3.20]])]:
                for q in qs:
                    for f in ([top_f] if k=='sleeve' else rays(m)):
                        F=B@f;pos=cen+B@q
                        add(k+str(j),tail=wrench(pos-d,-F) if k=='tail' else None,
                            roll=wrench(q,f),i=j,sl=wrench(pos,-F) if k=='sleeve' else None,
                            p=F[0] if k=='tail' else 0,c=-F[0] if k in ('wall','side') else 0)
        for pos in ((-14.30,-6.85) if direction.any() else ()):add('guide'+str(pos),sl=wrench(pos*X+9.65*direction,-direction+mu*X))
        add('drive',sl=wrench(off,-X))
        A=np.array(cols).T; ids=np.array(ids);P=np.array(P);C=np.array(C)
        for cap in ['tail45','cage45']:
            for k,v in dict(boxes,tension=(4*W,4*W,0,0,0,0,0),compression=(-20,-20,0,0,0,0,0),moment=(0,0,0,0,0,0,52.2)).items():
                lo=np.r_[v[0],-np.array(v[2:])];hi=np.r_[v[1],v[2:]]
                if k=='moment':lo[-1]=52.2
                R=linprog(-(ids==('drive' if peak_index is None else 'sleeve'+str(peak_index))).astype(float),A_ub=np.vstack([A[:6],-A[:6],P if cap=='tail45' else C]),
                    b_ub=np.r_[-lo,hi,45],A_eq=A[6:],b_eq=np.zeros(24),method='highs')
                key=cap+'_'+k
                if R.success and (key not in data or -R.fun>data[key]['F']):
                    z=R.x
                    data[key]=dict(F=-R.fun,pull=sum(z[ids=='drive']),signed_seat_adjustments=gaps.tolist(),center=off.tolist(),w=(-A[:6]@z).tolist(),tail=P@z,cage=C@z,res=max(abs(A[6:]@z)),
                         normals={tag:sum(z[ids==tag]) for tag in sorted(set(ids))})
    return data
def local_relax():
    # Continuous support-point boxes enclose tail and sleeve positions; pressure
    # in either x direction at each journal but NOT both in the same fitted slot.
    # Cylindrical ends angular drift <1.3 deg: x/r range conservatively .17.
    # One lower toe may contact opposite upper half when radial skew is nonzero.
    best={}
    for w0,w1,side,low in product((-1,1),(-1,1),(-1,1),(-1,0,1)):
        A=[]; ids=[]; fx=[];rforce=[]
        def block(k,dirs,px,py,pt):
            for q in product(px,py,pt):
                for f in dirs:
                    A.append(wrench(q,f));ids.append(k);fx.append(f[0]);rforce.append(f[1])
        # Tail effective normal among all +/-2deg rotations. Enclose true cone.
        nn=(X+Y)*c45
        cone=[nn+(f-nn)*tan(atan(mu)+rad(2))/mu for f in rays(nn,True)]
        block('tail',cone,[-1.15,-.965],[-1.15,-.965],[-1.53,1.53])
        tlo,thi=(-1.60,1.60) if low==0 else ((-.15,1.60) if low==-1 else (-1.60,.15))
        # Worst-case axial sliding; allow upper/lower stick/spin tangential component as well.
        block('upper',rays(-Y,True),[-.12,.12],[1.40,1.55],[tlo,thi])
        if low:block('lower',rays(Y,True),[-.12,.12],[-.56,-.43],[low*3.38,low*3.87])
        for s,w in [(-1,w0),(1,w1)]:
            # local x distance opposite inward wall normal
            block('wall',rays(w*X,True),[-w*.45,-w*.56],[-.14,.14],[s*2.79,s*3.40])
        block('side',rays(side*Z,True),[-.60,.60],[-.60,.60],[-side*3.84])
        ids=np.array(ids);A=np.array(A).T;fx=np.array(fx)
        # Normalize on true tail axial component or mechanical cage pull. When
        # cage includes an unknown external guide wrench, cap must be downstream.
        for k,obj in [('upper',ids=='upper'),('lower',ids=='lower'),('sum',(ids=='lower')|(ids=='upper'))]:
            E=(ids=='tail')*fx
            R=linprog(-obj.astype(float),A_eq=np.vstack([A,E]),b_eq=[0]*6+[1],method='highs')
            if R.success:best[k]=max(best.get(k,0),-R.fun)
            else:assert R.status==2
    return best
if __name__=='__main__':
    a=local_relax()
    # Pure axial slip in finite guide bands. Reactions radial toward common
    # axis, guide friction +x. Moment in yz plane equals (x_g+mu*Rg) X cross
    # radial reaction vector. Bound each force by solving the 2x2 system.
    pmin=6.25;R=9.65;Xr=[-4.42,-3.82]
    K=(max(abs(x+mu*R-z) for x in [-14.90,-13.70] for z in Xr)+
       max(abs(x+mu*R-z) for x in [-7.45,-6.25] for z in Xr))*hypot(1,mu)/pmin+2*8.85*mu/pmin
    print(json.dumps(dict(label='exploratory',actual=inside(),reset_actual=inside(.20),outer_per_axial_tail=a,ideal_center_feedback=0,
        two_single_resultant_bands_normal_K=K,tail45_lockland_outer_N=(1+K)*mu*45*a['sum']/(1-2*mu*.05/pmin),
        center_mismatch_0p05_feedback=2*mu*.05/pmin,
        notes='Outer only for stated bounded flat-land contact modes and actual tail-axial cap; no inference of 45 N cap on tail from a 45 N cage cap'),indent=2))
