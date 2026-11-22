from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 print('existing face: local x, radius/t, fixed except noted, in mm; disk rear and full flat',HOME-1.60,HOME, 'at terminal',HOME-1.60+TR,HOME+TR)
 f=chassis()+pads();e=json.loads((D/'shell-elec70.json').read_text());k=move(disk(),0.)
 # Certificate for a trial full circular home cylinder through moving plate
 # advance. Intended disk rear face is excluded: carrier may join there.
 # Minkowski translation of inserted volume, then compare to fixed stock.
 c=xy('trial center cavity',(-9.30,-8.57),0,0,0,6.92);s=sweep([c],TR*X)
 # Not grouping annular housings/skirts into filled stock. Use axial OR
 # radial per-sector supporting plane vs separate true convex pieces.
 static=f+drum()+e
 moving=curvesweep()
 def radial_gap(q):
  x=ext(q,X[None]);lo=ext(s[0],X[None]);a1=max(float((x[0]-lo[1])[0]),float((lo[0]-x[1])[0]))
  ds1=np.array([U(a) for a in np.arange(-180,180,.25)]);mn=ext(q,ds1)[0];return max(a1,float(max(mn)-6.92))
 print('axis cylinder R6.92, height .73, home x[-9.30,-8.57], translated 0..8.53. Min separation to fixed stock incl full ring blank/electronics',min((radial_gap(q),q[0]) for q in static))
 print('swept leaf and link stock vs translated pocket',min((radial_gap(q),q[0]) for q in moving))
 cs=[q for q in k if not q[0].startswith(('broad ejector',))];print('co-moving min radius lower for disk key/post/backer/live channels',min((max(ext(q,np.array([U(a) for a in np.arange(-180,180,.5)]))[0]),q[0]) for q in cs))
 print('center quill occupied x[-24.42,-9.39] r<=3.44; inner key webs x[-11.79,-9.32] r2.88..6.87 t±1.47 @ BAZ; side pads x[-11.81,-9.34] r6.53..8.05 t=±[1.16,1.50]. These are true metal inside the requested region, not shaft-hole allowances.')
 print('moving home posts x[-19.74,-8.43] r8.18..9.56 t±1.39, keys x[-20.31,-8.44] r6.99..8.29 t±1.05; backers x[-9.28,-8.51] r7.80..11.50 t±2.35; all advance +8.53 with disk.')
 print('no coaxial solid spring/cup length 7mm down the full R9 corridor. Annular/sector designs require azimuth, travel, preload reactions, walls, tool access and loss of room to pitch/yaw.')
if __name__=='__main__':run()
