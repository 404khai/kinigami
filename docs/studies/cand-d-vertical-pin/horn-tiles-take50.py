from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('horn-package-take50.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
cap49=json.loads((Path(__file__).resolve().parents[1]/'cand-d-forced-section/take49-low-cap-v3-sweep.json').read_text())
def tiles(name,relative=False):
    d=cap49['states'][name];return [mx(shp(s),-d['face_X'] if relative else 0.) for s in d['solids']]
def ts(a,b,relative=False):
    return [poly(s[0],s[1]+t[1]) for s,t in zip(tiles(a,relative),tiles(b,relative))]
def interior(a,b):
    # Inscribe both disks in their real surface. Positive common ball proves
    # overlap of solids. Never infer a crossing from envelope-only negatives.
    def inner(s):
        if s[3] is None:return np.array(s[1])
        return np.array(filldisk((s[0],s[1],s[2]*cos(pi/32),s[3]),32)[1])
    eq=np.vstack((ConvexHull(inner(a)).equations,ConvexHull(inner(b)).equations))
    res=linprog([0,0,0,-1],A_ub=np.c_[eq[:,:3],np.ones(len(eq))],b_ub=-eq[:,3],bounds=[(None,None)]*4,method='highs')
    return res.x
def runtiles():
    hw=allmotor()+cheeks50()+extra()[:1];xhw=lowfixed()
    for i,(a,b,n) in enumerate(cap49['phases']):
        s=ts(a,b);r=ts(a,b,True);lo,hi=((0.,0.) if i==0 else ((0.,PH) if i==1 else (PH,PH)))
        angles=rotor(lo,hi)+stages(lo,hi)
        print(n,'fixed upper / moving horn / fixed lower / moving lower / electronics',*(fastpair(A,B)[0] for A,B in ((s,hw),(s,angles),(s,xhw),(r,lowmoving()),(s,parts()))),flush=True)
    # Use specific time states (not union) for common-point certificates.
    candidates=[]
    for a,b,n in cap49['phases']:
        la,lb=tiles(a),tiles(b)
        for u in (0,.25,.5,.75,1):
            sm=[poly(s[0],map(tuple,np.asarray(s[1])*(1-u)+np.asarray(t[1])*u)) for s,t in zip(la,lb)]
            for s in sm:
                for obj in hw+parts()+xhw:
                    if obj[0].startswith(('lined radial','metal bearing','frame thrust')):continue
                    if any(sep(s,obj,d)>0 for d in (X,Y,Z)):continue
                    v=interior(s,obj)
                    if v[3]>.005:candidates.append((v[3],n,u,s[0],obj[0],tuple(v[:3])))
    print('state witnesses fixed-geometry intersections',sorted(candidates,reverse=True)[:6])
    m=material(parts())+[(s[0],q) for s in tiles('home') for q in s[1]]
    print('home material lower bound incl Take49 tiles',certify(m))
    q=np.array([(-28.7330054,14.64524095,10.7998831),(15.4,3.64,19.022),(12.3,9.75,-23.50),(-21.98788102,-15.65,-22.01767642)])
    w=np.array([.18137544,.35189829,.12099926,.34572701]);print('separate Take49 input four-point RMS diameter',2*sqrt(w@(q*q).sum(1)-sum((w@q)**2)))
if __name__=='__main__':runtiles()
