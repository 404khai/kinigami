"""Explore yaw installation before selecting the documented pose; surrogate scores only."""
from drive82 import *
from scipy.optimize import differential_evolution
def search():
 # Model x-directed actuator cylinders and radial cell/PCB planes. No scoring shortcut
 # counts as a full solid clearance test. Coordinates correspond to the straight pose.
 C=np.array([-21.02571,0,0])
 yp,zp=at(1,0)
 def rz(p,a):
  a=radians(a);t=p.copy();t[:,0]=p[:,0]*cos(a)-p[:,1]*sin(a);t[:,1]=p[:,0]*sin(a)+p[:,1]*cos(a);return t
 yz=[]
 for a,g in AXES:
  c,s=cos(radians(a)),sin(radians(a))
  for X0,X1,R,T,rad in [(-31.85,.45,14.5,7.92,3.0),(-41.5,-35.3,14.5,0,6.87),(-34.9,-26.65,14.5,0,4.55),(-24.5,-7.5,14.5,0,2.6),(-16.1,0,0,0,10.9)]:yz.append([X0,X1,R*c-T*s,R*s+T*c,rad])
 cy=np.array(yz)
 def pointscore(p,r):
  DX=np.maximum(cy[:,0]-p[:,0,None],p[:,0,None]-cy[:,1])
  DR=np.hypot(p[:,1,None]-cy[:,2],p[:,2,None]-cy[:,3])-cy[:,4]
  ds=np.hypot(np.maximum(DX,0),np.maximum(DR,0))+np.minimum(np.maximum(DX,DR),0)
  return np.max(np.maximum(0,r[:,None]-ds))
 za=np.arange(-17.,16.51,1.8)
 m=np.c_[np.full(len(za),2.82),np.full(len(za),-18.69),za]
 H=np.array([[0.,0.,z] for z in np.arange(-6.5,18.,1.3)]+[[0.,y,16.63] for y in np.arange(-14.,0,.8)])
 cb=[np.array([[-35.1,-.91],[11.12,19.77],[-9.1,9.1]]),np.array([[-36.,-1.12],[11.78,20.07],[-8.65,8.65]])]
 def fun(v,detail=False):
  x,y,a,ca,ba=v;p=rz(np.r_[m,H],a)+[x,y,0];r=np.r_[np.full(len(m),3.0),np.full(len(H),1.82)]
  bad=[pointscore(p,r),max(0,max(np.linalg.norm(p-C,axis=1)+r)-29.64)]
  for ang,b in zip([ca,ba],cb):
   c,s=cos(radians(ang)),sin(radians(ang))
   coord=np.c_[p[:,0],c*p[:,1]+s*p[:,2],-s*p[:,1]+c*p[:,2]]
   e=np.maximum(b[:,0]-coord,coord-b[:,1])
   bad.append(np.max(np.maximum(0,r-np.linalg.norm(np.maximum(e,0),axis=1)-np.minimum(np.max(e,axis=1),0))))
  return bad if detail else sum(v*v for v in bad)
 sol=differential_evolution(fun,[(-34,-26),(-8,8),(95,240),(187,197),(307,317)],seed=82,popsize=12,maxiter=100,tol=1.e-6)
 return sol.x,fun(sol.x,True)
if __name__=='__main__':print(search())
