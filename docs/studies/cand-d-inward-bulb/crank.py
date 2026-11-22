"""One geometry: L18 pivot toward local +t, with a rigid spherical nose.

Seated static screens. No roll sharing, guide, energy, or package credit.
da in the face proof bounds centre-tangent error, not ball spin.
"""
from math import asin, cos, pi, sin
import numpy as np
from tripod import R,X,Y,Z,f,integrated,envelope
from face_margin import certificate
from friction import dual
from mushroom import H,b,bh


def geometry(L=18.,h0=2.45):
    q=asin((H-h0)/L)
    gs=[]; axes=[]
    for point,normal,i,bore in integrated():
        theta=2*pi*i/3
        d=-sin(theta)*Y+cos(theta)*Z
        axes.append(np.cross(bore,d))
        tangent=cos(q)*bore+sin(q)*d if np.linalg.norm(bore) else bore
        gs.append((point,normal,i,tangent))
    return gs,axes


def cones(gs,axes,L=18.,mu=.23,nv=16,dn=.028,dp=.30,da=.012):
    groups=[]
    k=mu/cos(pi/nv)
    for (p,n,i,a),axis in zip(gs,axes):
        t=np.cross(X,n);t/=np.linalg.norm(t)
        t2=np.cross(n,t)
        spin=np.cross(axis,n)*b/L
        ac=a+spin
        cols=[]
        for j in range(nv):
            v=n+k*(t*cos(2*pi*j/nv)+t2*sin(2*pi*j/nv))
            cols.append(np.r_[v,np.cross(p,v)/R,ac@v*np.eye(3)[i]])
        # Rotate the complete outer cone to the uncertain true normal
        # by the minimum-angle rotation. Rotate the pole arm as well.
        # Extra errors: axle chord .008, L ±.05, sphere rad ±.01.
        dw=bh*(dn+.008)/(L-.05)+.01/(L-.05)+bh*.05/(L*(L-.05))
        acerr=(da+dw+np.linalg.norm(ac)*dn) if np.linalg.norm(a) else 0.
        e=np.hypot(1.,k)*np.r_[np.full(3,dn),np.full(3,(dp+np.linalg.norm(p)*dn)/R),
                                acerr*np.eye(3)[i]]
        groups.append((np.array(cols),e))
    return groups


if __name__=='__main__':
    gs,axes=geometry()
    for m,dn,F in ((70.,.012,30.),(90.,.028,32.),(110.,.028,35.)):
        nom=np.r_[np.zeros(6),np.full(3,F)]
        groups=cones(gs,axes,dn=dn)
        for case in ('service','table','fault'):
            e=np.r_[envelope(m,case,R,'take23'),[.8]*3]
            lo=min(certificate(gs,j,nom,e,dn=dn,da=.012) for j in range(9))
            ub=[dual(groups,nom,e,row) for row in np.eye(9)]
            print('g,dn,F,case,zero-friction lower,rear/V cone upper',
                  m,dn,F,case,round(lo,3),round(max(ub[::3]),3),
                  round(max(np.delete(ub,[0,3,6])),3))
