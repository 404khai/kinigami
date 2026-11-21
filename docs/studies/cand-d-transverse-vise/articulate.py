"""Adjacent-head yaw screen, Take 30. Units mm; use explicit component guards."""
from math import cos, hypot, pi, radians, sin, sqrt
import numpy as np


def rect(boxes,name,x,y,z):
    boxes.append((name,*[(a+b)/2 for a,b in (x,y,z)],*[(b-a)/2 for a,b in (x,y,z)]))


def cyl(boxes,name,axis,ctr,r,ends,outer):
    i='xyz'.index(axis); a,b=[j for j in range(3) if j!=i]
    for lo,hi in zip(np.linspace(-r,r,17)[:-1],np.linspace(-r,r,17)[1:]):
        d=max(0.,lo,-hi) if outer else max(abs(lo),abs(hi))
        half=sqrt(max(0.,r*r-d*d))
        if half<1e-9: continue
        bounds=[None]*3
        bounds[a]=(ctr[0]-half,ctr[0]+half)
        bounds[b]=(ctr[1]+lo,ctr[1]+hi)
        bounds[i]=ends
        rect(boxes,name,*bounds)


H=(-6.5,-7.8)
J=(H[0]+10.5*cos(radians(-98)),H[1]+10.5*sin(radians(-98)))


def head(outer=True,s=0.,lift=0.,cellx=-12.35,celly=-14.30,extras=(),fixed=False):
    h=[]
    def box(n,x,y,z): rect(h,n,x,y,z)
    def disk(n,axis,ctr,r,ends): cyl(h,n,axis,ctr,r,ends,outer)
    box('cell',(cellx,cellx+20.70),(celly,celly+30.65),(-20.40,-15.))
    box('blade',(3.35+s,4.15+s),(-1.5,9.25),(-10.65,10.65))
    for sg in [-1,1]:
        z=sorted((sg*11.4,sg*12.9))
        if not fixed:box('rack'+str(sg),(-17.5+s,8+s),(-8.05,-6.25),z)
        disk('platen-guide'+str(sg),'y',(.55,sg*5.5),1.5,(-6.,29.))
    # The bridge is an allocation, NOT all solid metal.
    box('bridge',(-2.1,19.),(3.5+lift,10.5+lift),(-7.1,7.1))
    if not fixed:
        disk('ejector shaft','z',(6.,-9.25),1.30,(-12.9,19.4))
        disk('ejector wheel','z',(6.,-9.25),7.9,(17.4,19.4))
    disk('ejector motor','z',(12.6,-15.37),3.2,(-17.9,10.8))
    disk('clamp motor','y',(-10.,16.),3.2,(-9.75,18.95))
    mid=(-10.603,10.03,4.) if fixed else (-4.276,14.203,4.)
    for j,(x,z,r) in enumerate([(-10.,16.,2.8),mid,(.55,0.,11.8)]):
        disk('clamp gear'+str(j),'y',(x,z),r,(-11.95,-10.75))
    disk('nut/thrust','y',(.55,0),4.75,(-16.8,-6.1))
    disk('screw','y',(.55,0.),1.25,(-6.1,29.))
    if fixed:
        disk('eject screw','x',(-11.5,16.9),1.,(-4.,20.45))
        box('joint motor',(J[0]-3.2,J[0]+3.2),(J[1]-3.2,J[1]+3.2),(-11.7,7))
        box('controller',(-11,11),(-8.9,8.9),(19.85,25.55))
    for name,x,y,z in extras:box(name,x,y,z)
    return h


def pairs(A,B,H,pitch,angles,interval=0.,clearance=.0):
    """Positive separation on a SAT axis excludes overlap. Reuse the
    axis at the interval midpoint with a Hausdorff debit to cover the arc.
    Negative SAT separation for inner boxes at zero debit is a witness
    of intersection of the represented solids (not of omitted details).
    """
    a=np.array([z[1:] for z in A]);b=np.array([z[1:] for z in B])
    ia,ib=np.nonzero(abs(a[:,None,2]-b[:,2])<a[:,None,5]+b[:,5]+clearance)
    if not len(ia): return {}
    x,y,_,w,h,_=a[ia].T;u,v,_,k,l,_=b[ib].T;u=u-H[0];v=v-H[1]
    budget=2*np.hypot(abs(u)+k,abs(v)+l)*sin(radians(interval)/4)+clearance
    out={}
    for angle in angles:
        t=radians(angle);c=cos(t);s=sin(t);cc=abs(c);ss=abs(s)
        dx=H[0]+pitch+c*u-s*v-x;dy=H[1]+s*u+c*v-y
        gaps=np.maximum.reduce((abs(dx)-w-cc*k-ss*l,abs(dy)-h-ss*k-cc*l,
                                abs(dx*c+dy*s)-k-cc*w-ss*h,abs(-dx*s+dy*c)-l-ss*w-cc*h))
        # Internal pair search filters intentionally co-bundled features
        # at its caller, never by an automatic component-name exemption.
        for j in np.flatnonzero(gaps<budget):
            key=(A[ia[j]][0],B[ib[j]][0]);gap=gaps[j]-budget[j]
            if key not in out or gap<out[key][0]: out[key]=(gap,angle)
    return out


def adj(H,angles,outer,s=0.,lift=0.,cellx=-12.35,celly=-14.30,extras=(),interval=0.):
    return pairs(head(outer,s,lift,cellx,celly,extras),head(outer,0.,0.,cellx,celly,extras),
                 H,30.,angles,interval)


if __name__=='__main__':
    trial=(-8.,-15.5)
    for cellx,celly in [(-14.,-15.325),(-12.35,-14.30)]:
        for lift,s in [(0.,0.),(21.5,0.),(21.5,15.)]:
            out=adj(trial,np.arange(-15.,15.01,.25),False,s,lift,cellx,celly)
            print('cell/pose',cellx,celly,lift,s,'inner witnesses at fixed pitch',
                  [(k,tuple(round(float(a),3) for a in v)) for k,v in sorted(out.items())])
    print('revised pivot and PMD axis',H,J)
    def family(h,*names):return [j for j in h if j[0] in names]
    def without(h,*names):return [j for j in h if j[0] not in names]
    h=head(fixed=True)
    # Bound ALL intermediate bridge heights by one extrusion of the bridge
    # allocation. Keep original retracted blade: its attachment and extension
    # depend upon the new nut/guide crosshead and the actual release trajectory.
    tall=without(h,'bridge');rect(tall,'bridge',(-2.1,19.),(3.5,32.),(-7.1,7.1))
    angle=np.arange(-14.875,15.,.25)
    for p in (30.,34.5):
        for name,h1 in [('stowed',h),('all bridge heights',tall)]:
            hits=pairs(h1,h,H,p,angle,.25,.20)
            print('revised adjacent component guards,',p,name,'unseparated:',list(hits))
            if p==34.5: assert not hits
    M=('joint motor','controller');moving=[]
    tx=15.-34.5
    for sg in [-1,1]:
        z=sorted((sg*6.3,sg*8.7))
        rect(moving,'arm',(tx+7,tx+12),(-1.2,1.2),z)
        rect(moving,'ear return',(tx+11.4,tx+12.6),(-8.,0.),z)
        rect(moving,'ear heel',(tx+11.4,H[0]),(-8.5,-7.1),z)
    for a in (180,60,-60):
        x=tx+7*cos(radians(a));z=7*sin(radians(a))
        rect(moving,'boss cube',(x-3,x+3),(-3,3),(z-3,z+3))
    rect(moving,'web',(tx-8.75,tx+7.4),(-1.2,1.2),(-8.7,8.7))
    rect(moving,'cap',(tx-10.45,tx-4),(-1.5,3),(-2,2))
    rect(moving,'top ball and bed',(tx-4.2,tx+4.2),(-3.6,3.6),(-4.2,4.2))
    cyl(moving,'pin','z',H,1.5,(-13.5,9.5),True)
    for name,fixed,m,poses,step in [
            ('motor and electronics',without(tall,*M),family(h,*M),[0.],0.),
            ('twin yoke, paddle and pin',tall,moving,angle,.25)]:
        e=pairs(fixed,m,H,0.,poses,step,.20)
        print('own-head unseparated guards,',name,list(e))
        assert not e
