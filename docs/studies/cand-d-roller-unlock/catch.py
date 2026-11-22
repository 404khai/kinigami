"""Rock until the remaining .050 radial relief is exhausted; test loads at that pose only."""
from travel import *
from roller import X,Y,Z,rays,wrench,linprog,np
def test():
    p=boss+1.75; r=6.45
    a=brentq(lambda a:sin(a)*(xc-p-Ro*tan(a))+r*cos(a)-h-1.5,0,.1)
    U=cos(a)*X-sin(a)*Y; V=sin(a)*X+cos(a)*Y
    center=(p+Ro*tan(a))*X; O=center-boss*U
    ring=p*X-Ro*Y; q=xc*X+r*Y-1.5*V
    # Round head on tangential roller touches t=0 only; application point exact.
    # Ring edge is tangent at -R_o; no line-of-pressure freedom off the point.
    A=np.array([wrench(ring-O,F) for F in rays(U,True)]+[wrench(q-O,F) for F in rays(-V,True)]).T
    k=A.shape[1]//2
    out={}
    for name,v in b.BOXES.items():
        lo=np.r_[v[0],-np.array(v[2:])];hi=np.r_[v[1],v[2:]]
        obj=np.r_[-A[0,:k],np.zeros(k)]
        R=linprog(obj,A_ub=np.vstack([A,-A]),b_ub=np.r_[-lo,hi],method='highs')
        out[name]=-R.fun
    w=-(wrench(ring-O,2.7*U)+wrench(q-O,-.5*V))
    assert np.all(np.abs(w)<=np.array([4*b.W,b.W,b.W,46*b.W,50.8*b.W,52.2]))
    return dict(label='exploratory',hard_contact_angle_deg=degrees(a),head_contact_body_x=boss+(q-center)@U,
           conditional_fixed_pose_upper_ring_axial=out,service_witness_external=w.tolist(),ring_normal=2.7,
           roller_normal=.5,front_cage_wall=.5*sin(a),relief_sleeve=.5*cos(a))
if __name__=='__main__':print(json.dumps(test(),indent=2))
