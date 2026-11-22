"""Take 73 trial. Coordinates (axial, outboard, tangential), lengths in mm."""
from math import *
import numpy as np

B,K,J,XB=14.56,.52,.25,-1.095
R,W,XA,XF=2.45,2.25,-1.04,-.125
SLOT=.050
XW,RW,XI=-.75,12.75,-.42
D=B+K*XI-(RW-.75*(XI-XW))
MU=.23
LAM=.46
ANG=radians(.20)
POSITION=.012

def b(x):return np.maximum(B+K*x,B+(K-J)*XB+J*x)
def w(x,t):return np.sqrt(b(x)**2-t**2)
def f(x):return RW-.75*(x-XW)+D
def lower(x,t):return np.maximum(w(x,t),f(x))

def metal(C,plug):
    # Actual witnesses on fixed stock. At each trial x,t choose nearest y
    # on the filled segment roof..19. Coordinates at cut edges are legal.
    cx,cy,ct=C.T;dist=np.full(len(C),np.inf)
    boxes=[(-6.95,XA-SLOT,-6.6,6.6,w),(XF+SLOT,0.,-6.6,6.6,w),
            (-6.95,0.,W+SLOT,6.6,w),(-6.95,0.,-6.6,-W-SLOT,w)]
    if plug:boxes.append((XA,XF,-W,W,lower))
    for xlo,xhi,tlo,thi,roof in boxes:
        r=np.hypot(cy,ct);px=(cx+K*(r-B))/(1+K*K)
        for trial in (cx,px,px-.25,px+.25,np.full_like(cx,XI),np.full_like(cx,XI+.075),
                      np.full_like(cx,XI+.16)):
            xx=np.clip(trial,xlo,xhi)
            for target in (ct,b(xx)*ct/r):
                tt=np.clip(target,tlo,thi); yy=np.clip(cy,roof(xx,tt),17.9)
                dist=np.minimum(dist,(xx-cx)**2+(tt-ct)**2+(yy-cy)**2)
    return dist

def cover(moving,side,corner=None):
    # Each terminal edge cone gets its own hemisphere cover. Parameter 0
    # follows the edge, parameters 1/2 are elevation / azimuth of n.
    xa,xf,tw=(XA,XF,W) if moving else (XA-SLOT,XF+SLOT,W+SLOT)
    U=(1. if moving else -1.);v=np.array([LAM,-float(moving),0.])
    xside=corner if corner else (side if side!='lateral' else None)
    ts=side=='lateral' or bool(corner)
    x0=xa if xside!='front' else xf;t0=tw if ts else 0.
    dx=0 if xside else xf-xa;dt=0 if ts else tw
    m=np.array([[.5,pi/4,0.]]);h=np.array([[.5,pi/4,pi]])
    speed=np.linalg.norm(v);nb=0;least=1e9
    for lev in range(55):
        nb+=len(m);s,el,a=m.T;ds,de,da=h.T
        x=x0+dx*s;t=t0+dt*s
        n=np.column_stack((np.cos(el)*np.cos(a),-np.sin(el),np.cos(el)*np.sin(a)))
        dn=de+da*np.cos(el-de)
        nv=n@v;work=nv-MU*np.sqrt(np.maximum(0.,speed**2-nv**2))
        # Projection length, like the normal itself, is 1-Lipschitz
        # in angular distance; norm of the two work coefficients is kappa.
        work-=hypot(1,MU)*speed*(dn+ANG)
        low=work<=(.10 if moving else .003)
        if (~low).any():least=min(least,work[~low].min())
        wt=w(x,t);F=f(x)
        # Conservative derivative enclosure, including either piece at
        # the crease, the vertical walls and all their endpoint normals.
        dw=(.54*dx+.18*dt)*ds;df=.75*dx*ds
        cf=(wt+dw>=F-df) if moving else np.ones(len(m),bool)
        bf=(F+df>=wt-dw) if moving else np.zeros(len(m),bool)
        sxlo=np.where(bf,-.75,K);sxhi=np.where(cf,.54,-.75)
        stlo=np.where(cf,-.18,0.);sthi=np.zeros(len(m))
        for j,gl,gh,sgn in [(0,sxlo,sxhi,(-U if xside=='rear' else U) if xside else 0),
                              (2,stlo,sthi,U if ts else 0)]:
            # sg=0: the horizontal component cannot be independently
            # supported. sg=+/-1: positive combination with that cut normal.
            du=(1+np.maximum(abs(gl),abs(gh)))*dn+1e-10
            if sgn<=0:low&=n[:,j]+gh*n[:,1]<=du
            if sgn>=0:low&=n[:,j]+gl*n[:,1]>=-du
        qy=lower(x,t)-D if moving else wt
        C=np.column_stack((x,qy,t))+R*n
        # A sphere at a higher point on the same side (or less extension)
        # only moves outboard. A material witness can follow it in y up to
        # 17.9, so the distance cannot increase while its center y<=17.9.
        dq=np.hypot(np.hypot(dx,dt)*ds,np.maximum(dw,df) if moving else dw)
        if low.any():
            low[low]=np.sqrt(metal(C[low],not moving))+dq[low]+R*(dn[low]+ANG)+POSITION+1e-9>=R
        if not low.any():return nb,least
        m=m[low];h=h[low]
        if lev==54 or len(m)>100000:raise ValueError((moving,side,corner,m[0],h[0],work[low].min()))
        dim=np.argmax(h*np.array([hypot(dx,dt)*1.3,R,R]),axis=1)
        rows=np.arange(len(h));h[rows,dim]/=2;shift=np.zeros_like(m);shift[rows,dim]=h[rows,dim]
        m=np.concatenate((m-shift,m+shift));h=np.tile(h,(2,1))

def datums():
    # Entire rounded hull versus bevel (unit support) and uninterrupted
    # rear taper. All other clocks and button capsules attain no larger
    # projection than these disk and endpoint supports.
    circles=[(-2.25,7.60),(.20,7.10),(2.50,6.),(4.40,3.50),(-.30,7.58),(2.25,6.50),(5.80,3.16)]
    bevel=max(.60*x+.80*y for x,y in circles+[(-2.25,10.75),(-4.31,5.15),(-2.25,5.15),(0.,2.50)])
    wall=min((B+(K-J)*XB+J*x-y)/hypot(1,J)-2.5 for x,y in circles+
             [(-2.25,10.75),(-4.31,10.30),(-2.25,10.30),(0.,5.)])
    assert abs(bevel+2.50-(.60*XW+.80*RW))<1e-9 and wall>0.
    disk=12.42;g=B-disk+.05;rgap=b(XI)-D-disk
    need=R-sqrt(R*R-g*g);pmin=1.43; pmax=1.73
    edge=acos(1-pmax/R)+radians(.6)
    print('stroke, fixed bore to rounded hull, minimum lip land on either side, disk radial reserve',
          D,wall,1.25*min(XW-XA,XI-XW),rgap)
    print('outer generator minimum forward rim, margin, upper rim useful fraction',
          need,pmin-need,cos(edge)-MU*sin(edge))
    for nx,ny,move in ((-.6,-.8,True),(K/hypot(K,1),-sqrt(1-(W/b(XA))**2)/hypot(K,1),True),
                       (J/hypot(J,1),0.,False)):
        dot=LAM*nx-int(move)*ny;speed=hypot(LAM,int(move))
        work=dot-MU*sqrt(speed**2-dot**2)-hypot(1,MU)*speed*ANG
        assert work>(.1 if move else .003)

if __name__=='__main__':
    datums()
    for mov in (True,False):
        for side,corner in [('rear',None),('front',None),('lateral',None),('lateral','rear'),('lateral','front')]:
            print(mov,side,corner,cover(mov,side,corner),flush=True)
