"""Trial containing sphere for proposed head extension. Not the G1 evaluator.
Translate frozen v7 nose forward and enclose its full interpolated sweep;
all original body/coupler solids stay enclosed, including the tail. No change
to declaration. A feasible witness proves fit of this subset, not the internals.
"""
import itertools,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation

def envelopes():
    d=json.loads((Path(__file__).resolve().parents[3]/'candidates/cand-d/declaration.json').read_text())
    if d['candidate_version']!=7:
        d=json.loads((Path(__file__).resolve().parents[3]/'candidates/cand-d/declaration-v7.json').read_text())
    shapes=[]
    for p in d['stowed_geometry']['primitives']:
        if p['role']=='cavity': continue
        q=p['pose']['orientation']
        A=Rotation.from_quat([*q[1:],q[0]]).as_matrix()
        c=np.array(p['pose']['position_um'])/1000
        moving=(p['role']=='coupler' and c[0]>0)
        if p['kind']=='box':
            ext=np.array(p['half_extent_um'])/1000
            points=c+np.array(list(itertools.product((-1,1),repeat=3)))*ext@A.T
            shapes.append((moving,'box',points))
        elif p['kind']=='cylinder':
            shapes.append((moving,'cyl',(c,A[:,2],p['radius_um']/1000,p['half_height_um']/1000)))
        else: raise NotImplementedError(p['kind'])
    return shapes

def far(c,shapes,extension):
    out=[]
    for moving,kind,data in shapes:
        for x in ((0,extension) if moving else (0,)):
            cc=c-np.array([x,0,0])
            if kind=='box': value=np.max(np.linalg.norm(data-cc,axis=1))
            else:
                centre,axis,r,h=data
                dv=cc-centre;ax=dv@axis
                value=math.hypot(abs(ax)+h,np.linalg.norm(dv-ax*axis)+r)
            out.append(value)
    return max(out)
if __name__=='__main__':
    shapes=envelopes()
    for e in (0,2.0,2.7,3.0):
        sol=minimize(lambda c:far(c,shapes,e),[11.72+e/2,0.,0.],method='Nelder-Mead',
                     options={'maxiter':2000,'xatol':1e-9,'fatol':1e-9})
        c=np.round(sol.x,3)
        d=2*far(c,shapes,e)
        print(f'extension {e:.2f}, witness centre {c}, containing diameter {d:.5f} mm')
    # Distance to a point is convex along the displacement, so endpoint bounds
    # also cover the intervening extrusion. They do not cover any larger holder.
