from verify75 import *
from scipy.spatial import HalfspaceIntersection
from itertools import product
dirs=np.unique(np.r_[ds,-ds,DD,-DD],axis=0)
POD=(('jaw',('jaw worm','jaw 32T','jaw 16T','jaw geared','jaw motor spindle','jaw thrust shoulder','jaw retained thrust collar','parking star')),
 ('brake',('dog geared','dog spindle','dog input spindle','dog input spur','dog driven spur','dog blind cam','dog outboard','dog spring cap','dog spring reserve','dog bush')),
 ('eject',('disk geared','disk worm shaft','disk worm blank','disk worm 32T','disk drive 16T','disk drive spindle','disk thrust bearing','disk nut journal','disk 24T','disk worm fixed bearing')))
def cases():
 # Convex shells assembled from preformed two halves. Outer hull is
 # defined by finite support halfspaces (not inscribed point samples).
 # .09 internal build clearance and .26 polymer skin are trial values.
 b=jawdrive()+ejectdrive()+park()+sweep(dogmove(3.03),2.04*Z);res=[]
 for n,ids in POD:
  ss=sel(b,ids);hi=np.max([ext(s,dirs)[1] for s in ss],0);center=np.mean([np.mean(s[1],0) for s in ss],0);pr=[]
  for st in (.09,.35):
   eq=np.c_[dirs,-hi-st];v=HalfspaceIntersection(eq,center).intersections;v=np.unique(np.round(v,9),axis=0);pr.append(sol(n+' cover '+str(st),v[ConvexHull(v).vertices]))
  res.append(tuple(pr))
 return res
def verts(s):
 pts=np.asarray(s[1]);h=ConvexHull(pts)
 ic={j:i for i,j in enumerate(h.vertices)};faces=[]
 for p,e in zip(h.simplices,h.equations):
  a,b,c=pts[p]
  if np.cross(b-a,c-a)@e[:3]>0:p=p[::-1]
  faces.append([ic[j] for j in p])
 return pts[h.vertices].round(7).tolist(),faces
def poly(q):
 p,f=verts(q);return 'polyhedron('+json.dumps(p,separators=(',',':'))+','+json.dumps(f,separators=(',',':'))+',convexity=6);'
def outf():
 cc=cases();f=['// Exploratory removable polymer 0.26 wall; WORLD X. Pre-cut blanks.','module podoutside(){union(){']+[poly(q) for i,q in cc]+['}}','module podinside(){union(){']+[poly(i) for i,q in cc]+['}}','module pods(){difference(){podoutside();podinside();}}']
 (D/'pods75.scad').write_text('\n'.join(f)+'\n')
 c=np.array([-1.07,.68,.50])
 print('gross convex fixed clam cover volumes, uncut (inner/outer mm3) and farthest world distance at trial center',[(q[0],ConvexHull(i[1]).volume,ConvexHull(q[1]).volume,far(q,c)) for i,q in cc])
 # Retest sphere using exact far of the finite cover vertices and the
 # previous full-yaw supports. Missing port cuts only reduce exterior.
 import verify75 as verify
 old=verify.allstock;verify.allstock=lambda:old()+[o for _,o in cc];verify.sphere()
 print('gross covered neighbors (outer blanks, separation negative inconclusive)');verify.peer()
 for q in ref['fixed']:
  if q[0].startswith('foot ('):floor=ext(q,np.eye(3))[0][2];break
 print('foot floor',floor,'fixed pod zmin',[(o[0],ext(o,np.eye(3))[0][2]-floor) for _,o in cc], 'nose guard ground margin',22.95*-1-floor)
if __name__=='__main__':outf()
