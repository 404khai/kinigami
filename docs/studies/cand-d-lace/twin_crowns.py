"""Machined twin crowns and six bounded flats; Take 54, exploratory mm."""
from itertools import product
import json
from math import cos,hypot,pi,radians,sin,sqrt
import sys
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull
from face import X,Y,Z,budget,setup

PITCH=38.
O=17.04*X
WIDTH=.90
ANGLE=60.
BASE=1.85
R=8.


def box(n,v):
    return n,np.asarray(v),0.,None


def stock():
    points,ns,_=setup(13.,radians(ANGLE),radians(-90))
    tail=[];head=[]
    for j,(p,n) in enumerate(zip(points+O,ns)):
        u=(p-O)/13;v=np.cross(n,u)
        q=p-BASE*n
        rim=np.array([q+WIDTH*(s*u+t*v) for s,t in product((-1.,1.),repeat=2)])
        # Outside bound on a round turned R8 cap. Crown at q;
        # actual edge depth R-sqrt(R²-w²), backing plane at .35 mm.
        r2=rim+.35*n
        root=np.array([p+2.5*X+s*.90*u+t*.85*np.cross(X,u)
                       for s,t in product((-1,1),repeat=2)])
        tail.append(box(f'crown{j}',np.vstack((rim,r2,root))))
        front=np.array([q+1.02*s*u+1.20*t*v for s,t in product((-1,1),repeat=2)])
        root=np.copy(front)
        root[:,0]=13.4
        head.append(box(f'flat{j}',np.vstack((front,root))))
    return head,tail,ns


def frame():
    def bar(name,a,b,w,h):
        p=np.array(a);q=np.array(b);v=q-p;v=v/np.linalg.norm(v)
        v=np.array([0.,-v[2],v[1]]);v/=np.linalg.norm(v)
        return box(name,[s+i*w*v+j*h*X for s in (p,q)
                         for i,j in product((-1,1),repeat=2)])
    def block(name,bounds):
        return box(name,list(product(*bounds)))
    f=[bar('lower cross',(13.4,-9.2,-14.9),(13.4,9.2,-14.9),1.5,1.48),
       block('lower pad',[(13.3,14.45),(-2.7,2.7),(-15.9,-12.48)]),
       bar('top cross',(13.1,-13,8.1),(13.1,13,8.1),1.55,1.6)]
    path=[(13.4,8.1,-15.1),(14.3,20.6,-7.4),(14.3,20.6,4.6),(12.8,12.,8.)]
    for i in range(len(path)-1):f.append(bar(f'side {i}',path[i],path[i+1],1.55,1.3))
    for s in (-1,1):
        p=np.array([13.1,s*11.258,6.5])
        f.append(box(f'cap {s}',[p+i*1.1*X+j*2.6*Y+k*2.5*Z
                                 for i,j,k in product((-1,1),repeat=3)]))
        a,b=sorted((s*5.5,s*9.0))
        f.append(block(f'top spine {s}',[(-5.7 if s<0 else -2.25,14.4),(a,b),(11.,11.95)]))
        f.append(block(f'top cleat {s}',[(11.85,14.4),(a,b),(9.1,11.2)]))
        if s<0:f.append(block('rear cleat',[(-5.7,-3.4),(a,b),(8.4,11.2)]))
    f.append(block('top yoke',[(-2.25,1.0),(-8.,8.),(11.,11.95)]))
    f.append(block('rear yoke',[(-5.7,-3.4),(-8.,-.2),(8.2,9.15)]))
    f.append(block('bridge tie',[(-5.7,-3.4),(-4.9,-3.2),(6.7,8.5)]))
    return f


def directions():
    a=np.arange(25)*pi/48; b=np.arange(96)*pi/48
    x,y,z=np.broadcast_arrays(np.cos(a[:,None]),np.sin(a[:,None])*np.cos(b),
                              np.sin(a[:,None])*np.sin(b))
    return np.c_[x.ravel(),y.ravel(),z.ravel()]


def project(shapes,d):
    hi=[];lo=[]
    for name,p,r,axis in shapes:
        p=np.array(p)@d.T
        offset=r if axis is None else r*np.sqrt(np.maximum(0.,1-(d@np.asarray(axis))**2))
        hi.append(p.max(axis=0)+offset);lo.append(p.min(axis=0)-offset)
    return np.array(hi),np.array(lo)


def overlaps(head,tail,d):
    # Positive lower bound for each nominal pair and the entire aligned
    # +X withdrawal ray. Nonpositive is inconclusive, not a collision.
    h,_=project(head,d);_,t=project(tail,d)
    return sorted((round(float(np.max(b-a)),5),n[0],m[0])
                  for n,a in zip(head,h) for m,b in zip(tail,t))


def screen(groups):
    h,t,ns=stock();d=np.vstack((directions(),ns));f=frame()
    print('head flats vs crown outer stock',overlaps(h,t,d)[:8])
    def mv(s):
        n,p,r,a=s
        return n,np.array(p)+PITCH*X,r,a
    T=[mv(s) for s in groups['straight_passive_tail_outer'] if not s[0].startswith('seat landing')]
    H=[s for s in groups['fixed'] if not s[0].startswith(('fixed face facet','face rear bridge','sill post'))]
    print('new flats vs inherited tail',overlaps(h,T,d)[:4])
    print('new crowns vs inherited head',overlaps(H,t,d)[:4])
    print('frame vs all mated tail',overlaps(f,T+t,d)[:4])
    df=np.vstack((d,-d))
    for group in ('fixed','split_throats_closed','split_throats_open','stripper_flush','rocker_reference','boards'):
        others=[s for s in groups[group] if not s[0].startswith(('face rear bridge','sill post','fixed face facet','sill to front'))]
        print('frame/flat vs',group,overlaps(f+h,others,df)[:4])
    for group in ('split_throats_closed','split_throats_open','stripper_flush','stripper_eject'):
        print(group,'vs new crowns',overlaps(groups[group],t,d)[:2])
    # Posed interference needs its own check; do not combine moving alternatives.
    print('nose sag, surrogate tail/head stock volumes (overlap not subtracted)',
          np.round([R-sqrt(R**2-WIDTH**2),sum(ConvexHull(s[1]).volume for s in t),
                    sum(ConvexHull(s[1]).volume for s in h)],3))
    print('frame volume upper mm3',round(sum(ConvexHull(s[1]).volume for s in f),2))
    for mass in (50.,70.,90.):
        print('mass, needed service/table/fault N (ratio 1.16, line cone 6.7deg)',
              mass,np.round(budget(mass,13.,ANGLE,(-6.,6.),1.16,port_angle=6.7,
                                   p=38.,x=-.54,clock=-90.,crown_shift=R-BASE),3))
    # Axial balance with every planar Coulomb reaction acting in +X.
    alp=radians(ANGLE+.6);mu=.23;E=213000.;nu=.29
    N=(60+5*.070*9.80665)/(cos(alp)-mu*sin(alp))
    radius=(.75*N*R/(E/(2*(1-nu**2))))**(1./3)
    print('60 N draw: upper one-pole normal / Hertz a / peak MPa / rim reserve',
          np.round([N,radius,1.5*N/(pi*radius**2),WIDTH-radius-.19-R*sin(radians(.6))],3))


def rocker_group(shapes,ang,dx,origin):
    a=radians(ang);rot=np.array([[cos(a),-sin(a),0],[sin(a),cos(a),0],[0,0,1]])
    return [(n,(np.array(v)-origin)@rot.T+origin+dx*X,r,rot@axis if axis else None)
            for n,v,r,axis in shapes]


def rocker_sweep(j):
    g=j['groups'];B=g['rocker_reference'];p=np.array(j['rocker_axis'])
    h,_,_=stock();f=frame()+h;d=directions()[::4];d=np.vstack((d,-d))
    F,_=project(f,d)
    far=np.array([max(np.linalg.norm(v-p,axis=1))+r for _,v,r,_ in B])
    # Relative X translation is affine in the support inequality: minimum
    # is at an endpoint, independently for each axis, before maximizing.
    # Rotation intervals of 1 deg cost 2*r*sin(.25 deg). Do not debit
    # translation again. Smaller bounds from a coarse direction grid still
    # prove separation; failed bounds are not proof of intersection.
    for lo,hi in ((0.,0.),(-2.,2.)):
        out=[]
        sh=np.minimum(d[:,0]*lo,d[:,0]*hi)
        for a in range(-17,18):
            _,b=project(rocker_group(B,a,0,p),d)
            for (name,*_),u in zip(f,F):
                z=np.max(b+sh-u,axis=1)-2*far*sin(radians(.25))
                i=np.argmin(z);out.append((round(z[i],5),name,B[i][0],a))
        print('rocker sweep: X interval, rigid-stock gap lower bound and limiting sample',lo,hi,min(out))


if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('take53-provisional.json')
    j=json.loads(path.read_text())
    screen(j['groups']);rocker_sweep(j)
