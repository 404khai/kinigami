"""Grouped installed allocations; nominal enclosures and two-body sweeps."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('bore-chain-take53.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from scipy.optimize import linprog
from itertools import permutations
def splitguide(d):
    ls=[]
    for sg,k in product((-1,1),(-1,1)):
        for i in range(8):
            a=i*pi/8;b=(i+1)*pi/8
            ls.append(sol('split throat '+str((sg,k,i)),[(x,sg*6+rr*cos(t),k*(d+rr*sin(t))) for x,rr,t in product((A[0]+1.44,F-.08),(1.65,2.38/cos(pi/16)),(a,b))]))
        ls.append(bx('throat crossbar'+str((sg,k)),(11.05,12.55),(min(0,sg*6)-.45,max(0,sg*6)+.45),tuple(sorted((k*(d+1.93),k*(d+2.72))))))
    return ls
def blinds(closed):
    z=0 if closed else 5.10
    return [cy('hard port blind'+str(k),0,(F-1.77,F-1.40),(k*6,z),2.74) for k in (-1,1)]+[bx('blind connecting limb',(F-1.78,F-1.41),(-6.,6.),(z+2.05,z+2.75))]
def additions():
    # Some gear envelopes coincide with their own shafts and seats by design.
    return [cy('draw output overload pack',0,(-4.95,-3.84),(0,-10.25),2.62),
            bx('draw series pickup',(1.0,4.25),(-1.2,1.2),(6.65,8.13)),
            bx('load bridge ADC',(4.30,6.90),(-1.45,1.45),(6.78,8.23)),
            bx('index push plate',(2.52,6.03),(4.72,6.25),(5.64,6.37)),
            cy('shutter sequencing quill',1,(-11.5,7.4),(13.4,-6.75),.88),
            bx('screw positive radial key',(-3.73,-3.02),(-5.10,-2.90),(-10.48,-10.02)),
            bx('screw index crosshead',(-4.12,-2.85),(-6.12,-4.82),(-10.91,-9.59)),
            bx('index cam reach reserve',(-4.12,7.90),(-6.42,-5.15),(-12.02,-10.84)),
            bx('draw rack switch',(-3.33,-1.85),(5.55,7.09),(3.96,5.48)),
            bx('latch flag readout',(1.40,3.17),(8.04,9.50),(1.04,2.58)),
            bx('split half drawbar',(10.85,12.20),(9.25,10.15),(-6.25,6.25))]
def pads():return [bx('foot'+str((x,y)),(x-1.30,x+1.30),(y-1.25,y+1.25),(-23.50,-21.40)) for x,y in product((-12.,11.),(-8.5,8.5))]
def mv(s,t,u):return trans(rot(s,t,A),[-u,0,0])
def home():return blinds(True)+fixed()+rocker()+trunk()+feedmotor()+outriggers()+shutter(0)+additions()+splitguide(0)+pads()
def eboard():
    pth=D/'bore-electronics-take53.json'
    return json.loads(pth.read_text()) if pth.exists() else []
def reduce(S):
    groups={};d=np.eye(3)
    for s in S:
        n=s[0];k=next((p for p in ['wheel side cover','split throat','U tube OD','tail pivot lug','sector web','tail sector hub','sealed wheel keeper','shoe magazine OD','eject hoop'] if n.startswith(p)),n)
        groups.setdefault(k,[]).append(s)
    out=[]
    for k,v in groups.items():
        if len(v)==1:out+=v;continue
        a=np.array([ext(s,d) for s in v]);out.append(bx(k+' box',*zip(a[:,0].min(0),a[:,1].max(0))))
    return out
def efind():
    # Coarse greedy search; orientations cover 90-degree permutations only.
    fixedS=blinds(True)+blinds(False)+fixed()+outriggers()+additions()+shutter(0)+shutter(1.55)+pads()+splitguide(0)+splitguide(3.3)
    fix=extlist(reduce(fixedS));motion=[]
    for ang in np.linspace(-YMAX,YMAX,9):
        for u in (0,ST):motion.append(extlist([mv(s,ang,u) for s in reduce(rocker())]))
    es=np.stack(motion);swept=np.stack((es[:,:,0].min(0)-1.25,es[:,:,1].max(0)+1.25),axis=1)
    st=np.stack([extlist([trans(s,[-u,0,0]) for s in feedmotor()+trunk()]) for u in (0,ST)]);swept=np.concatenate((swept,np.stack((st[:,:,0].min(0),st[:,:,1].max(0)),axis=1)))
    ta=np.stack([extlist([rot(s,t,H) for s in reduce(tail())]) for t in np.linspace(-pi/12,pi/12,9)])
    tt=np.stack((ta[:,:,0].min(0)-1.20,ta[:,:,1].max(0)+1.20),axis=1)
    a=np.concatenate((fix,swept,tt));idx=[j for j,d in enumerate(ds) if np.count_nonzero(d)<2 or (sum(abs(d))<1.75 and np.all(np.isclose(abs(d),0)|np.isclose(abs(d),1/sqrt(2))|np.isclose(abs(d),1/sqrt(3))))]
    a=a[:,:,idx];d=ds[idx];grid=np.array(list(product(np.arange(-19,19.1,1.5),np.arange(-24,24.1,1.5),np.arange(-21,21.1,1.5))))
    ee=[]
    for name,dd in [('cell',(30.66,20.7,5.40)),('MCU',(22,17.8,5.7)),('dual H-bridge',(9.8,8.8,1.87)),('cutoff',(6.85,6.2,1.95)),('joint driver',(6.2,5.8,2.05)),('connector',(3.35,2.9,2.8)),('wire reserve',(3.4,3,2))]:
        best=None
        for dim in sorted(set(permutations(dd))):
            h=np.array(dim)/2;pad=np.abs(d)@h;rad=np.linalg.norm(abs(grid)+h,axis=1)
            k=np.argsort(rad);k=k[(rad[k]<(best[0] if best else 40))&(grid[k,2]-h[2]>=-23.45)&(grid[k,0]+h[0]<=F-.12)]
            z=grid[k]@d.T
            for lo,hi in a:
                ok=np.any((z+pad+.32<lo)|(z-pad-.32>hi),axis=1)
                if not ok.all():k=k[ok];z=z[ok]
                if not len(k):break
            if len(k):best=rad[k[0]],grid[k[0]],h
        if best:
            rad,o,h=best;s=bx(name,*zip(o-h,o+h));ee.append(s);a=np.concatenate((a,[ext(s,d)]));print(name,'centre',o,'size',2*h,'rad',round(rad,3))
        else:print(name,'NO GRID PLACEMENT')
    (D/'bore-electronics-take53.json').write_text(json.dumps(ee,separators=(',',':'))+'\n')
def enc(S):
    # Enclose solid sets by using exact vertex/ball or disk support at fixed
    # centre (optimizer only improves the upper bound, no lower claim).
    def f(x):return max(far(s,x) for s in S)
    q=minimize(f,[-2.,.2,-.6],method='Nelder-Mead',options={'maxiter':170,'xatol':.005,'fatol':.005})
    return sh(q.x),2*f(q.x),sorted([(far(s,q.x),s[0]) for s in S],reverse=True)[:3]
def polyin(s):
    n,v,r,d=s;v=np.asarray(v)
    if r==0:return v
    if d is None:
        # inscribed balls, hence hull of inner support for capsules
        u=ds
    else:
        d=np.array(d);a=np.eye(3)[np.argmin(abs(d))];aa=np.cross(d,a);aa/=np.linalg.norm(aa);bb=np.cross(d,aa);u=np.array([cos(t)*aa+sin(t)*bb for t in np.arange(32)*pi/16])
    return (v[:,None,:]+r*np.concatenate((u,-u))[None,:,:]).reshape(-1,3)
def ball(s,t):
    m=np.r_[ConvexHull(polyin(s)).equations,ConvexHull(polyin(t)).equations]
    w=linprog([0,0,0,-1],np.c_[m[:,:3],np.ones(len(m))],-m[:,3],bounds=[(None,None)]*4,method='highs').x
    return w
def alloc():
    own=tail();a=rocker();j=fixed();fx=blinds(False)+outriggers()+splitguide(3.3)+shutter(0)+additions()+pads()+eboard()
    # Collision witnesses between actual unbored gearmotor cans and metal posts.
    print('home package without/with electronics',enc(home()+own),enc(home()+own+eboard()))
    print('feet floor',min(ext(s,np.eye(3))[0][2] for s in home()+own+eboard()))
    print('home active head vs passive own',pairs(a+j+fx+feedmotor(),own))
    e=extlist(j+fx);f=extlist(a);worst=[];hh=[];nt=[]
    near=reduce(home()+eboard())
    for ang in np.linspace(-YMAX,YMAX,9):
        for u in (0,ST):
            m=[mv(s,ang,u) for s in a]+[trans(s,[-u,0,0]) for s in feedmotor()];me=extlist(m)
            worst.append((*pairs(m,j+fx,me,e),degrees(ang),u))
            for yaw in np.linspace(-15,15,13):
                t=[rot(s,radians(yaw),H) for s in own]
                nt.append((*pairs(m,t,me),degrees(ang),u,yaw))
                # Adjacent module passive tail mates to this head; its head
                # rotates about H+P, not the mating port or this module's hinge.
                n=[trans(rot(s,radians(yaw),H),[P,0,0]) for s in near]
                hh.append((*pairs(m,n,me),degrees(ang),u,yaw))
    print('equalizer vs stationary own (negative is not collision proof)',min(worst))
    print('equalizer vs own articulated tail / vs next head',min(nt),min(hh))
    for desc,stage in [('stowed',home()+eboard()),('stripped',fixed()+rocker()+feedmotor()+shutter(1.55)+outriggers()+eboard())]:
        left=reduce(stage);ee=extlist(left)
        vv=[(*pairs(left,[trans(rot(s,radians(y),H),[P,0,0]) for s in near],ee),y) for y in np.arange(-15,15.01,1.5)]
        print('whole head vs adjacent '+desc,min(vv),'sampling debit .2+max radius*angle',.20+2*max(far(s,H) for s in near)*sin(radians(.375)))
    witness=[]
    for deg in (-degrees(YMAX),0,degrees(YMAX)):
        for u in (0,ST):
            cans=[trans(s,[-u,0,0]) for s in feedmotor() if s[0]=='feed gearmotor'] + [mv(s,radians(deg),u) for s in a if s[0] in ('magazine closed rear endcap','wheel bearing cheek1','wheel bearing cheek-1')]
            for s in cans:
                for t in j+fx+own:
                    if t[0].startswith(('U tube OD','return leg OD','fixed face facet reserve','split throat','eject hoop')):continue
                    if pairs([s],[t])[0]>0:continue
                    v=ball(s,t)
                    if v[3]>.004:witness.append((v[3],s[0],t[0],deg,u,sh(v[:3])))
    print('common solid ball on motor vs fixed non-bore parts',sorted(witness,reverse=True)[:5])
    for u in (0,ST):
        e1=enc([mv(s,YMAX,u) for s in a]+[trans(s,[-u,0,0]) for s in trunk()+feedmotor()]+j+fx+own)
        print('maximum rocker angle package at slide',u,'upper diameter',e1)
    phases={'fixed':fixed()+additions()+outriggers()+pads(),'straight_passive_tail_outer':own,'rocker_reference':a,'slide':trunk()+feedmotor(),
            'stripper_flush':shutter(0),'stripper_eject':shutter(1.55),'blind_open':blinds(False),'blind_closed':blinds(True),'split_throats_closed':splitguide(0),'split_throats_open':splitguide(3.3),'boards':eboard()}
    (D/'bore-model-take53.json').write_text(json.dumps(dict(units='mm',head_face_x=F,pitch=P,pivot=H.tolist(),rocker_axis=A.tolist(),separate_states=True,groups=phases),separators=(',',':'))+'\n')
if __name__=='__main__':
    import sys
    if 'search' in sys.argv:efind()
    else:alloc()
