"""Place stock boxes among convex swept solids; a gap always names a separating axis."""
from itertools import permutations, product
from math import cos, pi, sin, sqrt

import numpy as np


def orientations():
    seen=set()
    for a,b,c in permutations(np.eye(3)):
        for angle in (0.,30.,60.,90.,120.,150.):
            # Box yaw about the remaining axis, including all-face-up poses.
            t=angle*pi/180.
            frame=np.array((cos(t)*a+sin(t)*b,-sin(t)*a+cos(t)*b,c))
            key=tuple(np.round(np.abs(frame @ np.array([1.,2.7,9.])),8))
            if key not in seen:
                seen.add(key)
                yield frame


def axes():
    # A finite subset of axes suffices to CERTIFY a positive gap. Failure
    # to find one is inconclusive (these are not exact intersection axes).
    out=[]
    for a,b,c in product(range(-3,4),repeat=3):
        v=np.array([a,b,c])
        if not v.any() or v[np.flatnonzero(v)[0]]<0:continue
        v=v/np.linalg.norm(v)
        if all(abs(v@u)<1-1e-10 for u in out):out.append(v)
    return np.array(out)


def project(s,ns):
    _,points,r,axis=s
    c=np.asarray(points)@ns.T
    w=r if axis is None else r*np.sqrt(np.maximum(0.,1.-(ns@axis)**2))
    return c.min(axis=0)-w,c.max(axis=0)+w


def domain(origin,R,grid):
    t=grid*np.arange(-int(R/grid),int(R/grid)+1)
    return np.array(np.meshgrid(t,t,t,indexing='ij')).reshape(3,-1).T+origin


def fits(centres,h,frame,origin,radius,floor):
    # Squared distance to farthest of the eight true OBB corners.
    r=np.linalg.norm(abs((centres-origin)@frame.T)+h,axis=1)
    z=centres[:,2]-abs(frame[:,2])@h
    return centres[(r<=radius)&(z>=floor)]


def place(centres,ns,obstacles,shape,frame,gap=.30):
    # obstacles: label, min/max supports and extra motion/interpolation debit.
    e=abs(ns@frame.T)@(np.asarray(shape)/2)
    ia=np.array([np.argmax(abs(ns[:,i])) for i in range(3)])
    for name,lo,hi,debit in obstacles:
        if not len(centres):break
        a,b=lo-e-gap-debit,hi+e+gap+debit
        ixs=np.flatnonzero(np.all((centres>a[ia])&(centres<b[ia]),axis=1))
        if not len(ixs):continue
        # Chunking prevents an O(grid * axes) allocation for a large part.
        keep=np.ones(len(centres),dtype=bool)
        for ids in np.array_split(ixs,(len(ixs)+1023)//1024):
            q=centres[ids]@ns.T
            keep[ids]=np.any((q<=a)|(q>=b),axis=1)
        centres=centres[keep]
    return centres


def search(solids,dims,origin=(-3.,0.,0.),radius=29.8,floor=-23.1,grid=2.):
    ns=axes(); origin=np.array(origin); cc=domain(origin,radius,grid)
    obstacles=[(s[0],*project(s,ns),err) for s,err in solids]
    # Broad obstacles eliminate grid points sooner; order does not alter
    # the surviving set.
    obstacles.sort(key=lambda t:np.prod(np.sort(t[2]-t[1])[-3:]),reverse=True)
    out=[]
    h=np.asarray(dims)/2
    for frame in orientations():
        cc1=fits(cc,h,frame,origin,radius,floor)
        a=place(cc1,ns,obstacles,dims,frame)
        if len(a):out.append((a,frame))
    return out


def slices(solids,dims,origin,radius=29.8,floor=-23.1,grid=1.):
    """Enumerate non-empty Z intervals at each XY sample (no Z lattice)."""
    ns=axes(); origin=np.array(origin); h=np.asarray(dims)/2
    t=grid*np.arange(-int(radius/grid),int(radius/grid)+1)
    xy=np.array(np.meshgrid(t,t,indexing='ij')).reshape(2,-1).T+origin[:2]
    dxy=xy-origin[:2]
    pp=xy@ns[:,:2].T
    obs=[(*project(s,ns),debit+.30) for s,debit in solids]
    ia=np.array([np.argmax(abs(ns[:,i])) for i in range(2)])
    hzn=abs(ns[:,2])<1e-9; n=(~hzn); inv=1./ns[n,2]
    out=[]
    for frame in orientations():
        corners=(np.array(list(product((-1,1),repeat=3)))*h)@frame
        dd=dxy[:,None,:]+corners[:,:2]
        rr=radius**2-np.sum(dd**2,axis=2)
        root=np.sqrt(np.maximum(0,rr))
        L=np.maximum(np.max(-root-corners[:,2],axis=1)+origin[2],floor-min(corners[:,2]))
        U=np.min(root-corners[:,2],axis=1)+origin[2]
        ok=(rr.min(axis=1)>0)&(L<U); cuts=[[] for _ in xy]
        e=abs(ns@frame.T)@h
        for lo,hi,g in obs:
            a,b=lo-e-g,hi+e+g
            ids=np.flatnonzero(ok & np.all((xy>a[ia])&(xy<b[ia]),axis=1))
            if not len(ids):continue
            p=pp[ids][:,hzn]
            ids=ids[np.all((p>a[hzn])&(p<b[hzn]),axis=1)]
            if not len(ids):continue
            p=pp[ids][:,n]
            a1=(a[n]-p)*inv; b1=(b[n]-p)*inv
            l=np.maximum(np.minimum(a1,b1).max(axis=1),L[ids])
            u=np.minimum(np.maximum(a1,b1).min(axis=1),U[ids])
            done=(l<=L[ids])&(u>=U[ids]); ok[ids[done]]=False
            mask=(l<u)&(~done)
            for i,j,k in zip(ids[mask],l[mask],u[mask]):cuts[i].append((j,k))
        verified=[]
        for i in np.flatnonzero(ok):
            l=L[i]; end=U[i]
            for a,b in sorted(cuts[i])+[(end,end)]:
                if a-l>.0001:verified.append([*xy[i],(l+a)/2])
                l=max(l,b)
        if verified:out.append((np.array(verified),frame))
    return out


def stock(name,c,dims,frame):
    v=(np.asarray(list(product((-1,1),repeat=3)))*np.asarray(dims)/2)@frame+c
    return name,tuple(map(tuple,v)),0.,None


def certificate(box,solids):
    ns=axes(); lo,hi=project(box,ns); gs=[]
    for s,debit in solids:
        a,b=project(s,ns)
        gs.append((max(np.maximum(a-hi,lo-b))-debit,s[0]))
    return min(gs)
