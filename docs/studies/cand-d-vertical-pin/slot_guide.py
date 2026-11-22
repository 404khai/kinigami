"""Five independently slotted guide rollers: quasi-static loss screen, N and mm."""
from itertools import product
from math import atan, cos, hypot, radians, sin
import numpy as np

X,Y,Z=np.eye(3)


def screen(offset=9., span=12., width=8., side=.23, roll=.005, lower=0.,
           home=False, roller=(2.,.85), drive_xy=None, moving=False):
    # Centres relative to the pin axis. Tracks are on the moving carriage;
    # each fixed roller may touch either side, NOT both at once. No axial
    # rub of the fork/shoulder credited. This is a guide coupon, not a Kin.
    pts=np.array([[-offset,-width,0],[-offset,width,0],[-offset,0,span],
                  [-offset,0,0],[-offset,width,span]])
    pts[:,2]+=lower
    if moving:
        pts[3:,1]=width/2
    normals=np.array([X,X,X,Y,Y])
    axes=np.cross(Z,normals)
    G=np.array([np.r_[n[:2],np.cross(p,n)/span] for p,n in zip(pts,normals)]).T
    H=np.linalg.inv(G)
    dtheta=2*sin(radians(.10)/2)
    radius,half_width=roller
    drive_point=np.r_[[-offset,0.] if drive_xy is None else drive_xy,0.]
    E=np.zeros((5,5))
    for i,row in enumerate(H):
        f=np.r_[row[:2],0.]; m=row[2:]/span
        for j,(p,n,ax) in enumerate(zip(pts,normals,axes)):
            # Normal at either radial side. Include any pressure centroid
            # across roller width; charge tangential wrench at that SAME
            # eccentricity. Absolute row bounds may overstate load.
            for s,t in product((-1,1),repeat=2):
                pt=p+s*radius*n+t*half_width*ax
                g=f+np.cross(m,pt)
                shape=.06*np.linalg.norm(m)*hypot(1,side+roll)
                extra=dtheta*(1+side+roll)*np.linalg.norm(g)
                E[i,j]=max(E[i,j],abs((g-(f+np.cross(m,p)))@n)+
                           side*abs(g@ax)+roll*abs(g@Z)+extra+shape)
    v=np.linalg.solve(np.eye(5)-E,np.ones(5))
    if min(v)<=0 or max((E@v)/v)>=1:return None
    # Dual for c·Q: if every roller bears on exactly one wall, s is its
    # sign vector and (I-E)Q <= diag(s) H b. Maximise over all signs,
    # including zero-load rollers. Use one external wrench per atom of
    # pressure; independently maximising every row spuriously adds loads.
    W=np.zeros((6,2))
    verts=np.array([[x*r,y*r,z+h] for x,y,h in product((-1,1),(-1,1),(0.,) if moving else (0.,12.7))
                   for z,r in ((-.85,.26),(11.90,4.32))])
    beta=atan(.32)
    e=cos(beta)*X+sin(beta)*Z
    pole=np.array([-(.48+.32*4.2*sin(beta)),0.,4.2*sin(beta)])
    for i,obj in enumerate(np.vstack((np.ones(5),np.eye(5)))):
        dual=np.linalg.solve((np.eye(5)-E).T,obj+1e-8)
        assert min(dual)>0 and np.all(dual-E.T@dual>obj)
        for s in product((-1,1),repeat=5):
            row=(dual*s)@H; f=np.r_[row[:2],0.]; m=row[2:]/span
            if home:
                g=f+np.cross(m,pole)
                # Compare to a reference normal e; dtheta debits both the
                # normal and tangent directions. Per N of normal, not P.
                load=(g@e+.23*np.linalg.norm(np.cross(e,g))
                      +2*sin(radians(2.)/2)*(1+.23)*np.linalg.norm(g)
                      +.47*hypot(1,.23)*np.linalg.norm(m))
            else:
                load=hypot(1,.23)*max(np.linalg.norm(f+np.cross(m,verts),axis=1))
            W[i,0]=max(W[i,0],load)
            W[i,1]=max(W[i,1],abs((f+np.cross(m,drive_point))@Z))
    a=atan(.32)-radians(1)
    lift=sin(a)-.23*cos(a)
    drag=(roll+dtheta*(1+side+roll))*W[0]
    return (W[0],W[1:,0].max(),lift-drag[0],1-drag[1],W[1:])


if __name__=='__main__':
    for side in (0,.10,.23):
        for z in (10.,14.,18.):
            s=screen(span=z,side=side)
            print('lateral traction, support span',side,z,'no bound' if s is None else
                  'sum Q/N,Q/D; max Q/N; lift/N; drive/D: '+
                  str(np.round([*s[0],*s[1:4]],5)))
    for label,roller in [('CFS1.4WV',(2.,.85)),('CFS2.5W',(2.5,1.5))]:
        W=screen(span=14.,lower=6.,home=True,roller=roller,drive_xy=(0.,0.))
        N=91.194/(cos(radians(2))-.23*sin(radians(2)))
        fz=sin(beta:=atan(.32)+radians(2))+.23*cos(beta)
        d=(fz+(.005+2*sin(radians(.1)/2)*1.235)*W[0][0])*N/W[3]
        bound=W[4]@np.array([N,d])
        S=screen(span=14.,lower=6.,roller=roller)
        print(label,'registered N; dog D and roller Q upper bounds',round(N,3),round(d,3),np.round(bound,2),
              'unlocked net coefficients',np.round(S[2:4],5))
