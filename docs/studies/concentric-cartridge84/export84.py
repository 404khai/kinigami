"""Optional editable OpenSCAD polyhedron export. Not used by any checks."""
from body84 import *
import argparse
def main():
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['LOCK','DRAW','UNLOCK','PARK','EJECT'],default='LOCK');p.add_argument('--fraction',type=float,default=0.);p.add_argument('--yaw',type=float,default=0.);p.add_argument('--output',default='inspect84.scad')
 a=p.parse_args();assert 0<=a.fraction<=1 and abs(a.yaw)<=15
 b=book();m=pose(b,a.phase,a.fraction,a.yaw,True)
 with open(a.output,'w') as f:
  f.write('// Take 84 EXPLORATORY; mm. Surface display is not a clearance test.\nshow_cover=false; show_guest=false; show_air=false;\n')
  for n,q in m.items():
   _,g,mt,k=b[n];me=q.simplify(.001).to_mesh64();vv=me.vert_properties[:,:3];tt=me.tri_verts[:,::-1];color='purple' if g=='guest' else 'royalblue' if g=='yaw' else 'tomato' if g!='fixed' else 'silver'
   cond='if(show_guest) ' if g=='guest' else 'if(show_cover) ' if mt=='PA12' else 'if(show_air) ' if k=='air' else ''
   f.write('// '+n+'\n'+cond+'color("'+color+'") polyhedron(points='+json.dumps(np.round(vv,5).tolist(),separators=(',',':'))+',faces='+json.dumps(tt.tolist(),separators=(',',':'))+');\n')
if __name__=='__main__':main()
