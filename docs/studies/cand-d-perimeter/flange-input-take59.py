"""Exact intersections for Take58 frozen convex tooth: (x,r,t) mm."""
from itertools import combinations
from pathlib import Path
from math import hypot,atan,degrees
import numpy as np,json
xr=-2.25+2.50*.38/hypot(1,.38);rr=10.75+2.50/hypot(1,.38)
# a dot p <= b
planes=np.array([[1,0,0,-.38],[-1,0,0,3.50],[0,0,1,3.20],[0,0,-1,3.20],[0,1,0,16.60],
                 [-.38,-1,0,-rr-.38*xr],[2.20,-1,0,-14.514-2.20*.38],[0,-1,1.05,-11.33],[0,-1,-1.05,-11.33]])
v=[]
for i in combinations(range(len(planes)),3):
 M=planes[list(i)];A=M[:,:3];b=M[:,3]
 if abs(np.linalg.det(A))<1e-11:continue
 x=np.linalg.solve(A,b)
 if np.all(planes[:,:3]@x<=planes[:,3]+1e-9):v.append(x.tolist())
J=dict(clock=-90,stroke=1.45,closed_pin_radius=17.45,bridge_xmax=-.81,normal_from_axis_deg=degrees(atan(1/.38)),tip_x=xr,tip_to_pin_radius=17.45-rr,aperture=[-3.61,-.27,3.31],roof_slope=.38,convex_blend=.12,halfspaces=planes.tolist(),prisms={'Take58 contact shoe ':v})
(Path(__file__).parent/'flange-jaw-take59.json').write_text(json.dumps(J,separators=(',',':'))+'\n')
