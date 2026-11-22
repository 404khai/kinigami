from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-electrics70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cell():
 z=[bx('cell bulk',( -15.4,15.4),(-8.4,8.4),(-2.7,2.7))]
 r=1.55
 for t in (-3.55,3.55):
  vv=[np.array([14.5,t,0])]+[np.array([15.72+r*sin(th),t,r*(1-cos(th))]) for th in np.linspace(0,pi,9)]+[np.array([15.72-(7-1.22-pi*r),t,2*r])]
  for j,(l,h) in enumerate(zip(vv,vv[1:])):
   z.append(sol('folded tab '+str((t,j)),[p+np.array([0,w,0]) for p,w in product((l,h),(-1.15,1.15))],.155))
 z+=[bx('tab insulator',(11.01,16.81),(-5.61,5.61),(2.73,2.88)),bx('protection board',(10.40,15.91),(-5.75,5.75),(3.33,4.43)),bx('spot joint reserve',(14.23,15.83),(-5.03,5.03),(2.99,3.48))]
 return z
