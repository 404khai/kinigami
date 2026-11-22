from package79 import *
from functools import lru_cache
from scipy.spatial import HalfspaceIntersection,distance
def covers():
 r=regions()
 # Fixed two-piece inspection enclosure over all actuator reservations,
 # including the swept lock arm circle and continuously expanding springs.
 # Halfspaces support it at fixed .30 inner, .72 outer perpendicular offset.
 # Fixed bore open only over x>=-9.68; aft fork window x<=-23.60.
 Csp=r['head']+r['shell']+r['front']+r['rear']+r['input']+r['coil']+r['index']+[ax('whole latch orbit',2,-14.04,14.04,LC,E0+1.19)]
 # No giant single convex machine envelope for mass. This covers DRIVE
 # only, cell and yaw remain independent with their own unresolved shell.
 dw=np.r_[ds,-ds]
 v=np.max(np.asarray([ext(q,dw)[1] for q in Csp]),axis=0)
 cen=np.array([-15.,11.,0.]);vi=HalfspaceIntersection(np.c_[dw,-v-.30],cen).intersections
 vo=HalfspaceIntersection(np.c_[dw,-v-.72],cen).intersections
 return dw,v,vi,vo
def zone(p): # no cut debits if wholly OUTSIDE both accessibility openings
 x,y,z=p
 return (x< -9.68 or hypot(y,z)>14.10) and (x>-23.60 or hypot(y,z)>10.85)
def capcheck():
 dw,v,vi,vo=covers();# windows, continuous fixed skin minus explicit cylinders
 # For the bypass, the BODY beyond the mating tail lies ahead at x>=...
 # Bound drive skin by exact outer polytope. Treating the full blank as
 # solid is conservative for separation to independent outside objects.
 return sol('uncut cover blank for outer support',vo)
