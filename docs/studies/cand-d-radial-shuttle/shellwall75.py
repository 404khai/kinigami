from covers75 import *
def run():
 cs=cases();ei=[ConvexHull(i[1]).equations for i,o in cs];eo=[ConvexHull(o[1]).equations for i,o in cs]
 # Actual continuous steel stock outside all face cutter paths; include
 # distance to its z-independent annular and axial boundaries. Retain
 # one finite ball inside a polymer skin and OUTSIDE every pod void.
 best=(-1,None)
 for ax in np.arange(-6.98,-5.07,.08):
  p=np.array([pos(t,ax,r) for t,r in product(np.arange(0,360,.5),np.arange(21.16,21.60,.063))]);rr=np.linalg.norm(p[:,1:],axis=1)
  slack=np.minimum.reduce((rr-21.15,21.60-rr,p[:,0]-O+7.025,O-5.035-p[:,0]))
  inn=np.min([(p@e[:,:3].T+e[:,3]).max(1) for e in ei],axis=0)
  for j,e in enumerate(eo):
   out=-(p@e[:,:3].T+e[:,3]).max(1);q=np.minimum.reduce((slack,inn,out));k=q.argmax()
   if q[k]>best[0]:best=(q[k],(p[k].round(5).tolist(),cs[j][1][0]))
 print('finite ball: untouched rotating ring and actual stationary polymer skin (+ means blocked; nonpositive is inconclusive)',best)
 # Bracket the 70Nmm loss case without stacking peak spring at an
 # incompatible lead. Pin remains area engaged at midstroke, star reaction
 # persists if the main drive does not unload it. Pinning force based on
 # full 70Nmm opposite torque applied at parking shaft, no worm friction.
 a=62;theta=(a-4)/116*pi;up=2.04*(1-cos(theta))/2;J=2.04*pi*sin(theta)/(2*radians(116));k=79000*.19**4/(8*1.39**3*6)
 # At this physical pose leading tip z=7.82+1.02=8.84: .82 in the hole.
 force=.23*70/2.08+.13+up*k
 print('same-pose adverse extraction at peak lead, actual shank remaining mm, force N, torque Nmm, optimistic 3V rated ceiling',min(1.46,9.66-(7.82+up)),force,J*force,.156*64*.70)
if __name__=='__main__':run()
