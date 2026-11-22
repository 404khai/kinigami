"""Local regression checks, not empirical or Gate evidence."""
import numpy as np
from crank import geometry, envelope, R, b
from tripod import matrix
from friction import missing_rear_witness
from face_margin import certificate, errgrad
from traction import maps, penalty, upper

gs,axes=geometry()
J=matrix(gs)
J2,costs=maps(gs,axes,0.,0.,dp=0.,da=0.)
assert np.max(abs(J2-J))<1e-12
nom=np.r_[np.zeros(6),[32.]*3]
err=np.r_[envelope(90,'table',R,'take23'),[.8]*3]
# Closed-form support of the EXACT frictionless matrix over the full box.
inv=np.linalg.inv(J.T)
expected=inv@nom-abs(inv)@err
actual=np.array([certificate(gs,i,nom,err,dn=0.,dp=0.,da=0.) for i in range(9)])
assert min(expected)>0 and np.max(abs(expected-actual))<1e-5
J,costs=maps(gs,axes,.23,.028)
for v in (np.arange(-4.,5.),np.sin(np.arange(9)),np.cos(np.arange(9))):
    lower=(J-penalty(costs,v))@v
    for j,((p,n,s,a),axis) in enumerate(zip(gs,axes)):
        # Exact minimum over tangential disk at nominal coordinates from
        # force-point kinematics, independent of the support-map factoring.
        g=v[:3]+np.cross(v[3:6]/R,p)+v[6+s]*(a+b*np.cross(axis,n)/18.)
        assert lower[j]<=n@g-.23*np.linalg.norm(g-n*(n@g))+1e-12
    dg=errgrad(gs,v,.028,.30,.012)
    assert min(dg@v)>0
caps=np.array([upper(J,costs,nom,err,j) for j in np.eye(9)])
lo=np.array([certificate(gs,i,nom,err,dn=.028,da=.012) for i in range(9)])
assert 1.7<min(lo)<1.9 and min(caps-lo)>0
assert max(caps[::3])<214 and max(np.delete(caps,[0,3,6]))<148
from tripod import integrated
assert missing_rear_witness(integrated())[0]==0.
print('nominal box support, force-point kinematics, dual bounds and empty-pad witness: OK')
