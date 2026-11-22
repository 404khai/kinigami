from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-check64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from scipy.optimize import brentq
def tilt():
 B=np.column_stack((X,U(-90),U(0)));A=np.array([[.932946637763,.351244332667,.078980946162],[-.360005614425,.911753138703,.197742690506],[-.002555126195,-.212916962301,.977066957017]]).T
 dst=O*X+B@np.array([6.3750494,4.3624475,.9742661]);M=B@A@B.T
 def tr(S):return [sol(s[0],dst+(np.array(s[1])-C*X)@M.T,s[2],None if s[3] is None else M@np.array(s[3])) for s in S]
 angle=brentq(lambda th:phase(th)[0]+.012,10,44);print('partial pose ring deg, determinant',angle,np.linalg.det(M))
 et=json.loads((D/'drum-model64.json').read_text())['electronics'];f=fixture();st=state(angle);h=efgroup(coarse(f+st))+et
 std=shift(h,P)
 # No undocumented replacement of adjacent pivot: the tail holds its pose;
 # adjacent powered body may pivot at joint HY_world in the transformed frame.
 for a in (-15.,0.,15.):
  post=tr(shift(rotate(h,a),P));fl=min((ext(s,np.eye(3))[0][2],s[0]) for s in post);print('adjacent joint yaw, powered-to-powered gap, floor lowest, intrusion',a,pairs(h,post),fl,-23.50-fl[0])
  foot=tr(shift(rotate(pads(),a),P));print('actual lowest neighbouring foot',min((ext(s,np.eye(3))[0][2],s[0]) for s in foot))
 others=[s for s in h if not s[0].startswith(('cone patch','fixed heel roof','fixed flared wall','bearing outer reserve','thin cheek liner','solid advancing disk','65deg drafted seat'))]
 for t0 in (0.,-.40,.22):
  t=tr([trans(q,t0*X) if q[0].startswith(('revised tail button','button plunger','button inner guide stem','captive button foot','plunger target ring')) else q for q in tail()])
  print('tilted full tail vs auxiliary stock outer',t0,pairs(others,t))
 # A continuum floor witness independent of neighbouring joint yaw, via
 # the entire nominal vertical-foot height interval across sample points.
 q=shift(pads(),P);minmax=[]
 for a in np.arange(-15,15.01,.5):
  mm=tr(shift(rotate(pads(),a),P));minmax.append(min(min(np.array(s[1])[:,2]) for s in mm))
 rad=max(far(s,H) for s in pads());print('global continuous worst clearance UPPER of a foot to plane vs all adjacent yaws',max(minmax)+2*rad*sin(radians(.125))+23.50)
if __name__=='__main__':tilt()
