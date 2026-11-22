from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-load64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def tests():
 ang=phase(0)[0];cx,x,r,qx,p=pole(ang);qr=sqrt(1-qx*qx);E=hingept(HX+1.35,HR+2.7,0,ang,0)-O*X;rx=x-E[0];ry=r-E[1];wx=x-HX;wy=r-HR;uj=np.array([x,r])
 for N in (410,534):
  nn=np.array([qx,qr]);tt=np.array([-qr,qx]);F1=N*nn;dist=hypot(rx,ry);mh=wx*F1[1]-wy*F1[0];me=rx*F1[1]-ry*F1[0]
  eadd=.23*N*abs(rx*tt[1]-ry*tt[0]);hadd=.23*N*abs(wx*tt[1]-wy*tt[0])
  print('jaw normal, centred frictionless E torque / high with μ=.23; best equal two bars shear MPa for BOTH load cases',N,me,abs(me)+eadd,abs(me)/(pi*.22**3),(abs(me)+eadd)/(pi*.22**3))
  print('jaw contact shear per equally loaded R.22, hinge T normal/upper, max required one horn axial N',N/(2*pi*.22**2),mh,abs(mh)+hadd,(abs(mh)+hadd)/(HORN*cos(ang)))
 for N in (197,261):
  fx=N*cos(FACE);ft=N*sin(FACE);fmax=fx+.23*ft;th=abs(ft+.23*fx);T=10.3*th
  print('one seat normal / clean axial and tangential / individual axial+, tangent+ including μ=.23 (not simultaneous)',N,fx,ft,fmax,th)
  A=np.vstack((np.ones(3),np.array([DR*U(a)[1:] for a in BAZ]).T))
  xp=-4.31-2.5*cos(FACE);r=10.3*U(BAZ[0])+(2.5*sin(FACE)+(xp+10.11)*tan(FACE))*U(BAZ[0]+90)
  f3=fx*np.linalg.solve(A,np.r_[1.,r[1:]])
  print('clean bilateral roller loads xg=-10.11, frictionless shaft bending worst, key torsion',f3,4*max(abs(f3))*(DR-9.49)/(pi*.73**3),10.3*ft)
  # Gross drafted seat insert base bending only; force point relative root.
  tb=2.5*sin(FACE)+(HOME-xp)/tan(FACE);w=3.81-tb;b=2.7;My=ft*(xp-HOME)+fx*(2.5*sin(FACE)-(3.81+tb)/2)
  print('uncut seat plan footprint, direct+bending gross root MPa',w*b,fx/(w*b)+6*abs(My)/(b*w*w))
 # Compressive yield and Hertz remain open beyond these gross sections.
 xq=-4.31-2.5*cos(FACE);wtop=3.81-1.95/tan(FACE)-(2.5*sin(FACE)+(-5-xq)/tan(FACE));print('65deg seat crest tangent, radial width',wtop,2*(1.35-1.95/tan(FACE)))
 s=next(q for q in disk() if q[0].startswith('65deg drafted seat') and q[0].endswith(', 1)'))
 xyz=pos(BAZ[0],xq,10.3,2.5*sin(FACE));pl=np.unique(np.round(ConvexHull(np.array(s[1])).equations,11),axis=0);k=np.argmax(pl[:,:3]@xyz+pl[:,3]);n=pl[k,:3]
 for rb in (.25,.50):
  ctr=xyz-rb*n;v=-(pl[:,:3]@ctr+pl[:,3]+rb);p=np.sqrt(np.maximum(0,1-(pl[:,:3]@n)**2));print('finite flat pole patch after corner rounding',rb,min(v[p>1e-4]/p[p>1e-4]))
 # Same-sign 3 DOF travel intervals must overlap; these are TRUE force
 # ranges before drag, independent of endpoint electrical state.
 desired=np.array([-.13135,.13135])
 for offsets in ([0,0,0],[-.09,0,.09],[-.15,0,.15]):
  L=max(desired[0]-np.array(offsets));Uu=min(desired[1]-np.array(offsets));print('three installed midlength errors, common physical interval width',offsets,Uu-L)
 # Check nearest REPEATED groove in 2D instead of subtracting cap radii on
 # just the arc axis (which would miss the offset X of opposite endcaps).
 for key,rs,rr in [('disk',DR,1.045),('leaf',16.675,.86)]:
  th=np.linspace(-3.75,106.5,661);ar=np.array([[-rs*radians(u), -19.03+phase(u)[1] if key=='disk' else -16.8+horn(phase(u)[0])[0]-HX] for u in th]);sep=min(np.min(np.linalg.norm(ar-z-np.array([rs*radians(120),0]),axis=1)) for z in ar)
  dd=np.gradient(ar,axis=0);dd2=np.gradient(dd,axis=0);curv=np.abs(dd[:,0]*dd2[:,1]-dd[:,1]*dd2[:,0])/np.linalg.norm(dd,axis=1)**3;print('two neighbouring grooves centreline / opposed-cut / min curvature radius sampled',key,sep,sep-2*rr,1/max(curv))
if __name__=='__main__':tests()
