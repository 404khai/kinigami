"""Mated stationary tail vs ancillary stock and finite seat/edge/load details."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-short62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cap(n):
 # Segment-polygons drawn through actual inscribed circle stations; use for
 # inner collision witnesses, never as an outer bound on absent interference.
 return frust(n,(C+1.95,C+4.50,C+8.05),(10.08,9.,5.66),inner=True)
def mated():
 ta=[innerfl()]+flange()[1:4]+[cap('actual broad socket')]+flange()[5:7]
 for p in (0,5.9,10,16):
  h=laws(p)[1];s=laws(p)[0];fixed=fixed2()
  rails=[q for q in fixed if q[0].startswith(('screw front anchor','fixed pivot reaction','fixed fork rear','fixed rocker pin','motor quill','clamp gearmotor'))]
  arm=[q for a in RK for q in rocker(a,p) if 'rocker' in q[0] or 'arm' in q[0]]
  brackets=[q for q in shell2() if 'output fork root' in q[0] or 'guide tie' in q[0] or 'extension foot' in q[0]]
  aux=rails+arm+shift(brackets,-h)
  o=flange();print('aligned mated full passive stock vs screw, actuated arms and positive sleeve bearings',p,pairs(aux,o)[:3])
  print('aligned mated inner stock vs ancillary real material',p,cp(aux,ta)[:2])
  m=shortstate(p)+fixed;print('forwardmost full listed powered housing vs local lip',p,max((ext(q,np.eye(3))[1][0]-O,q[0]) for q in m))
 # Post-release tilting is NOT assigned to the original tail pivot. Apply
 # trial rotations about passive rim centre and test against that same package.
 aux=fixed2()+shortstate(16)
 # For fixed contacts with held tail, existence of a separated position is
 # not proof of a path to it. Exclude intended seat interfaces in this screen.
 filt=[q for q in aux if ('pivot reaction spine' in q[0] or 'frame' in q[0] or 'clamp gearmotor' in q[0] or 'screw front anchor' in q[0] or 'fork root' in q[0] or 'guide tie' in q[0])]
 for ya in (-15,0,15):
  for x in (0,1.4,4.):
   out=shift([rot(q,radians(ya),C*X) for q in flange()],x)
   print('trial yawed held/withdrawn passive tail vs subset at park',ya,x,pairs(filt,out))
 # Closed moment from a still-engaged opposing fork: actual motor cylinder
 # and true fork solids, not a broad filled tail bound.
 motor=[q for q in fixed2() if q[0]=='clamp gearmotor'];fork=shift(flange()[5:7],-P)
 for a in (-15,0,15):print('own fork steel vs clamp motor',a,cp(rotate(fork,a),motor)[:1])
def grooves():
 # Profiles of the rotating first layout. Units mm; cylinder tracks use
 # unwrapped arc y=R*azimuth (radians) and x as the second coordinate.
 o={}
 for n,rad,rr in [('masterInner',17.1,.92+.065),('outerRetract',21.,.89+.065),('faceRadial',17.55,1.01+.065)]:
  v=[]
  for j in np.linspace(-2.,TH+2.,437):
   s,h,p=law(j);t=radians(-j)
   if n=='masterInner':v.append((rad*t,AX0-LEAD*j/TH))
   elif n=='outerRetract':v.append((rad*t,FX+h))
   else:v.append(((rad+s)*cos(t),(rad+s)*sin(t)))
  ar=np.array(v);dd=np.gradient(ar,axis=0);nn=np.c_[-dd[:,1],dd[:,0]]/np.linalg.norm(dd,axis=1)[:,None]
  o[n]=dict(frame='ring XY' if n=='faceRadial' else 'cylinder unwrapped arc,x',stations_deg=AZ if n=='faceRadial' else (tuple(a+14 for a in AZ) if n=='outerRetract' else (AIN,)),rad=rad,roller_clear_halfwidth=rr,profile=[z.round(5).tolist() for z in (ar,ar-rr*nn,ar+rr*nn)])
 (D/'sleeve-barrel-profile62.json').write_text(json.dumps(o,separators=(',',':'))+'\n')
def combined():
 # Endpoint and transition bound: use a single centre and point-set hull
 # incl all intermediate press positions (and all sweep uncertainty).
 q=json.loads((D/'sleeve-short62.json').read_text())
 print('straight complete all-motion common sphere upper',enc(osweep()+q['electronics']+shift(flange(),-P)))
 print('short fixed pin offset, outboard wall nominal radial reserve',RA-2.14-15.73)
if __name__=='__main__':mated();grooves();combined()
