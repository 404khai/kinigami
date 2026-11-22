from survey84 import *
from scipy.optimize import minimize
def main():
 b=book();m=pose(b,'LOCK',0,15);th=radians(15);rot=np.array([[cos(th),sin(th),0],[-sin(th),cos(th),0],[0,0,1]])
 x0,x1=1.70-PITCH,2.95-PITCH;ex=bb(m['eject M3 screw'])[[0,3]]
 def margins(q):
  z=rot@(q-PIV)+PIV
  return np.array([z[0]-x0,x1-z[0],10.35-np.linalg.norm(z[1:]),q[0]-ex[0],ex[1]-q[0],1.10-np.linalg.norm(q[1:]-EC)])
 # A feasible point, not an optimization lower bound: independently recompute every strict material clearance.
 test=minimize(lambda w:-w[3],[-38.4,-4.95,2.23,.2],constraints=[dict(type='ineq',fun=lambda w:margins(w[:3])-w[3])],method='SLSQP',options=dict(ftol=1e-12))
 pt=np.round(test.x[:3],6);ma=margins(pt);r=floor(min(ma)*100)/100-.01;assert r>.25
 dump('witness84.json',dict(label='exploratory',phase='LOCK',own_yaw_deg=15,common_ball_center=pt.tolist(),common_ball_R=r,minimum_face_clearances_mm=ma.tolist(),solids=['own solid tail flange','eject screw continuous R1.10 inner core of modeled R1.496 shaft'],polygon_overlap_mm3=(m['own flange']^m['eject M3 screw']).volume(),note='Using the smaller cylindrical core avoids relying on M3 thread crest material. Rotation inverted into flange-local frame; rigid coordinates mm. Full analytic cylinders and planar end faces, not an AABB or hollow-bearing witness.'))
if __name__=='__main__':main()
