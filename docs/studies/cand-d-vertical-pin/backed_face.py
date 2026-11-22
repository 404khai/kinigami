"""Six backed seats with a larger working radius. Exploratory; lengths mm."""
from itertools import product
from math import cos,hypot,pi,radians,sin,sqrt,tan
from pathlib import Path
from runpy import run_path
import numpy as np
from scipy.spatial import ConvexHull
from button_seats import X,Y,setup,test

RADIUS,STATION,ANGLE=14.5,7.,58.
K=.29


def lands(radius=RADIUS,station=STATION):
    _,_,_,b,ns=setup(-90.,radius,station,ANGLE)
    faces=[]
    for j,(p,n) in enumerate(zip(b-4.2*ns,ns)):
        u=np.cross(n,X);u/=np.linalg.norm(u);v=np.cross(n,u)
        h=.85
        verts=np.array([p+h*(a*u+d*v) for a,d in product((-1,1),repeat=2)])
        xb=5.5 if j>=2 else 5.8
        assert xb<verts[:,0].min()
        base=np.array([[xb,*(q[1:]+K*(q[0]-xb)*np.array([cos(a),sin(a)]))]
                       for q,a in product(verts,np.arange(8)*pi/4)])
        faces.append((f'land{j}',np.vstack((verts,base))))
    return b[::2],ns,faces


def beams(faces):
    # A full front face under each nose cap. Rear caps remain actual stock.
    def frustum(name,front,xr,xb,ya,yb,za,zb):
        def row(x):
            d=K*(xb-x)
            return [[x,y,z] for y,z in product((ya-d,yb+d),(za-d,zb+d))]
        p=np.array(row(xr)+row(xb))
        if front is not None:
            for v in front:
                assert min(np.min(v[:,1]-ya),np.min(yb-v[:,1]),
                           np.min(v[:,2]-za),np.min(zb-v[:,2]))>.015
        return name,p
    a=[v[4:] for _,v in faces]
    out=[]
    def bounds(v):
        return (np.min(v[:,1])-.12,np.max(v[:,1])+.12,
                np.min(v[:,2])-.12,np.max(v[:,2])+.12)
    f=np.vstack(a[:2]); y0,y1,z0,z1=bounds(f)
    out.append(frustum('bottom',a[:2],4.8,5.8,-17.6,17.6,z0,z1))
    for sg in (1,-1):
        f=a[2:4] if sg>0 else a[4:]
        lo,hi,_,zmax=bounds(np.vstack(f))
        out.append(frustum(f'side{sg}',f,4.8,5.5,lo,hi,z0+.4,zmax))
    # Crown pusher on the front of a lower rib. Pad stands behind rear-most
    # torus material x=3.30; no tracking of a loose eye is assumed.
    name,p=frustum('centre',None,1.65,2.90,-2.0,2.0,z1-2.0,.12)
    p[:,0]-=.30*p[:,2]
    out.append((name,p))
    return out


def lines(b):
    t=np.linspace(0,2*pi,241);circle=np.stack((15+7.5*np.cos(t),7.5*np.sin(t),0*t),axis=1)
    out=[('eye',q,p,7.5*(1-cos(pi/240))) for q,p in zip(circle,circle[1:])]
    def add(i,verts):
        for j,(p,q) in enumerate(zip(verts,verts[1:])):
            a=np.linspace(p,q,17)
            out.extend((f'{i}/{j}',v,w,0.) for v,w in zip(a,a[1:]))
    add('stem',[(22.5,0,0),(26,0,0)])
    add(0,[b[0],(22.5,0,0)])
    for i,p in enumerate(b[1:],1):
        x=18.75
        add(i,[p,(x,p[1],p[2]),(x,p[1],0.),(x,np.sign(p[1])*sqrt(7.5**2-(x-15)**2),0.)])
    return out


def face_check(b,ns,model):
    ls=lines(b);tags=np.array([j for j,*_ in ls])
    a=np.array([p for _,p,q,e in ls]);d=np.array([q for _,p,q,e in ls]);err=np.array([e for _,p,q,e in ls])
    th=np.arange(37)[:,None]*pi/72;ph=np.arange(72)[None,:]*pi/36
    D=np.stack(np.broadcast_arrays(np.cos(th),np.sin(th)*np.cos(ph),np.sin(th)*np.sin(ph)),axis=-1).reshape(-1,3)
    D=np.vstack((D,ns)); proj=np.minimum(a@D.T,d@D.T)
    for i,(name,p) in enumerate(model):
        # All axes have nonnegative X, so the same bounds hold on the
        # entire aligned forward ray of the tail relative to the face.
        gaps=(proj-(p@D.T).max(axis=0)).max(axis=1)-4.2-err
        mask=(tags!=f'{i//2}/0') if name.startswith('land') else np.ones(len(a),bool)
        if name.startswith('land'):
            n=ns[i]
            partner=min(np.minimum(a[~mask]@n,d[~mask]@n))-max(p@n)-4.2
            assert partner> -1e-12
        g=gaps[mask].min()
        print(name,'aligned nonpartner',round(g,4),tags[mask][gaps[mask].argmin()])
    for name,p in model:
        # Hood expands toward -X. Test the whole s in [-1.5,16.8].
        side=np.max([np.min((sg*p[:,1]-(8.26-.30*(p[:,0]-1.5)))/hypot(1,.30)) for sg in (-1,1)])
        bottom=np.min((7.53675+tan(radians(28))*(p[:,0]-1.5-12.389796)-p[:,2])*cos(radians(28)))
        h=ConvexHull(p)
        # Rear closures are not forward normals; count them as separate faces.
        fwd=h.equations[:,0]
        print(name,'hood plane, positive and rear facet normal x',round(max(side,bottom),4),
              round(np.min(fwd[fwd>0]),4),round(np.min(fwd),4))


def package(b,model):
    g=run_path(str(Path(__file__).with_name('horn-package-take48.py')))
    f=[g['poly'](name,list(map(tuple,p))) for name,p in model]
    ext=g['fp'](f)
    print('face vs retained joint',g['fastpair'](ext,g['joint48']())[:5])
    print('face vs stowed non-tail horn drive',g['fastpair'](ext,g['che5']()+g['fork5'](0,.62))[:3])
    # A candidate for a shifted joint motor is not a remounted drive.
    ob=[s for s in g['joint48']() if s[0] in ('yaw gearmotor','yaw saddle','yaw motor quill','yaw pinion 18T','quill nose bush')]
    for ang in (55.,80.,110.,140.):
        v=np.array([7.5*cos(radians(ang)),7.5*sin(radians(ang))])
        v+=np.array([-3.5,11.25])-np.array([3.7,13.35])
        moved=[g['move'](s,(*v,0.)) for s in ob]
        print('yaw motor angle and face gap',ang,g['fastpair'](moved,ext)[:1])


if __name__=='__main__':
    b,n,f=lands();model=f+beams(f)
    face_check(b,n,model);package(b,model)
    j=.070*9.80665*3*(37.5+18.566)
    v=test(-90.,RADIUS,STATION,ANGLE,5.62,.81,70.,(j,1.4*j))
    print('service/table/fault draw',np.round(v[1],3))
