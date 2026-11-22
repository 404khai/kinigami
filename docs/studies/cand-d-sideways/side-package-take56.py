"""Generic 3D package screens; use separate moving-state inputs, world mm."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('side-geom-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import json
from itertools import permutations
D=Path(__file__).parent
P=38.;H=np.array([-5.9,0.,0.]);F=16.50
V=json.loads((D.parent/'cand-d-forced-section/take51-interface-v3.json').read_text())
def shift(S,a,b=0,c=0):return [trans(s,[a,b,c]) for s in S]
def rotate(S,ya):return [rot(s,radians(ya),H) for s in S]
def boxesweep(S,dv):
    return [sol(s[0],s[1]+trans(s,dv)[1],s[2],s[3]) for s in S]
def ecc(f,mu,L,e,g):
    # Absolute worst-sign eccentricity of thrust and drag wrt thrust axis.
    k=2*mu/L
    return f*(1+k*e/(1-k*g)) if k*g<1 else inf
def elec(stock):
    # Only axes and diagonal support directions; positive separation is safe.
    # stock input already contains swept supports; minimize maximum range.
    hax=np.array([i for i,d in enumerate(ds) if np.count_nonzero(d)<2 or np.all(np.isclose(abs(d),0)|np.isclose(abs(d),1/sqrt(2))|np.isclose(abs(d),1/sqrt(3)))])
    dirs=ds[hax];a=extlist(stock)[:,:,hax]
    grid=np.array(list(product(np.arange(-20,17.1,1.5),np.arange(-23,24.1,1.5),np.arange(-21,21.1,1.5))))
    ss=[]
    for lab,dims in [('cell',(30.66,20.70,5.40)),('computer',(22,17.8,5.7)),('H-bridge',(9.8,8.8,1.87)),('cutoff',(6.85,6.2,1.95)),('joint driver',(6.2,5.8,2.05)),('connector',(3.35,2.9,2.8)),('wire reserve',(3.4,3,2))]:
        best=None
        for dim in sorted(set(permutations(dims))):
            h=np.array(dim)/2;pad=np.abs(dirs)@h;rad=np.linalg.norm(abs(grid)+h,axis=1);k=np.argsort(rad)
            k=k[(rad[k]<(best[0] if best else 41))&(grid[k,2]-h[2]>=-23.4)&(grid[k,0]+h[0]<=F-.15)];vv=grid[k]@dirs.T
            for lo,hi in a:
                ok=np.any((vv+pad+.32<lo)|(vv-pad-.32>hi),axis=1)
                if not ok.all():k=k[ok];vv=vv[ok]
                if not len(k):break
            if len(k):best=rad[k[0]],grid[k[0]],h
        if best:
            rad,o,h=best;s=bx(lab,*zip(o-h,o+h));ss.append(s);a=np.concatenate((a,[ext(s,dirs)]));print(lab,'centre',o,'size',2*h)
        else:print(lab,'NO GRID PLACEMENT')
    return ss
def bore_band(n,ax,span,cen,ri,ro,step=18):
    out=[]
    for i in range(step):
        v=[]
        for t,r,w in product([2*pi*i/step,2*pi*(i+1)/step],[ri,ro/cos(pi/step)],span):
            u=[cen[0]+r*cos(t),cen[1]+r*sin(t)];u.insert(ax,w);v.append(u)
        out.append(sol(n+str(i),v))
    return out
def planar_bush(n,span,x,z,r):return cy(n,1,span,(x,z),r)
def pads():return [bx('foot'+str((x,y)),(x-1.30,x+1.30),(y-1.25,y+1.25),(-23.50,-21.40)) for x,y in product((-12.,11.),(-8.5,8.5))]
def reduce(S,prefix=('tail sector hub','sector web','tail pivot lug','C shell tile','plug tile','face facet','gallery tile','pressure nut shell')):
    sets={};out=[]
    for s in S:sets.setdefault(next((u for u in prefix if s[0].startswith(u)),s[0]),[]).append(s)
    for k,v in sets.items():
        if len(v)==1:out+=v;continue
        e=np.array([ext(s,np.eye(3)) for s in v]);out.append(bx(k+' envelope',*zip(e[:,0].min(0),e[:,1].max(0))))
    return out
def cert(a,b):
    # Independent solid *inner* polytopes; use only on actual full stock.
    ea=extlist(a);eb=extlist(b);w=[]
    for i,s in enumerate(a):
        near=np.where(np.maximum(ea[i,0]-eb[:,1],eb[:,0]-ea[i,1]).max(1)<0)[0]
        for j in near:
            t=b[j];q=ball(s,t)
            if q[3]>.001:w.append((round(float(q[3]),5),s[0],t[0],tuple(round(x,5) for x in q[:3])))
    return sorted(w,reverse=True)
