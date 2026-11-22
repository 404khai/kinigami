"""Outer separation, inscribed material witnesses and a bare sleeve control."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-model62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def inner_ring(name,lo,hi,ri,ro,n=48):
 return [washer(name+str(j),(O+lo,O+hi),(ri,ri),(ro,ro),360*j/n,360*(j+1)/n,True) for j in range(n)]
def innerfl():
 return sol('true flange inner',[C*X+R*U(j*360/48) for j in range(48)],RE)
def cp(a,b,threshold=.005):
 ea=extlist(a);eb=extlist(b);out=[]
 for i,s in enumerate(a):
  w=np.maximum(ea[i,0]-eb[:,1],eb[:,0]-ea[i,1]).max(1)
  for j in np.flatnonzero(w<-threshold):
   q=ball(s,b[j])
   if q is not None and q[3]>threshold:out.append((round(float(q[3]),6),s[0],b[j][0],sh(q[:3])))
 return sorted(out,reverse=True)
def continuous(head,tail,head2=None):
 rs=max(far(q,H) for q in (head if head2 is None else head2));rt=max(far(q,H) for q in tail)
 yv=[];tt=[];eb=extlist(head)
 for ya in range(-15,16):
  n=shift(rotate(head if head2 is None else head2,ya),P)
  yv.append((*pairs(head,n,eb),ya));tt.append((*pairs(head,rotate(tail,ya),eb),ya))
 for n,li,r in [('head-head held pitch 38',yv,rs),('own revised tail-head',tt,rt)]:
  print(n,'raw / net lower',min(li),min(li)[0]-.20-2*r*sin(radians(.25)))
def grip():
 f=fixed();tail=shift(flange(),-P);tt=compress(tail[:7]);hd=swept()
 fn='biased' if BIAS else 'rigid'
 e=json.loads((D/('sleeve-'+fn+'62.json')).read_text())['groups']['boards']
 for th in (0,44,105):
  print('stow test th',th,'full',enc(f+state(th)+tail+e),'mechanical only',enc(f+state(th)+tail))
  print('min floor',min(ext(s,np.eye(3))[0][2] for s in f+state(th)+tail+e))
 continuous(hd+e,tt)
 print('boards versus all head sweeps',pairs(e,hd))
 # Bare rigid annulus + plate, no common drive or external guide. Keeps
 # inherited hinge/frame and the shoes, actual wall with windows.
 h0=plate()+[sol(*s) for s in V['joint']]+pads()
 js=[q for a in AZ for q in jaw(a) if q[0].startswith(('Take58','shoe broad'))]
 op=[trans(q,ST*U(a)) for a in AZ for q in jaw(a) if q[0].startswith(('Take58','shoe broad'))]
 walls=[s for s in lip() if s[0].startswith('conical lip')]
 bare=h0+boxesweep(compress(walls),-TR*X)+sum((boxesweep([q for q in js if q[0].endswith(' '+str(a))],ST*U(a)) for a in AZ),[])+boxesweep(op,-TR*X)
 eb=elec(bare+sum((rotate(compress(tail),a) for a in (-15,0,15)),[]))
 print('bare control straight stow only closed/parked',enc(h0+walls+js+tail+eb),enc(h0+shift(walls+op,-TR)+tail+eb))
 continuous(bare+eb,tt)
def witnesses():
 f=fixed();j=[sol(*s) for s in V['joint']];m=[q for q in f if q[0]=='clamp gearmotor'];rp=inner_ring('barrel intact radial middle ', -16.88,-5.98,18.10,19.95)
 flat=plate();seat=[s for s in flat if s[0].startswith('60deg')];ownt=shift([innerfl()]+flange()[1:4],-P)
 for th in (0,44,75,105):
  s,h,n=law(th);blank=shift(rp,-h)
  print('true barrel core v original fixed joint, own ger/shaft',th,cp(blank,j)[:2],cp(blank,m)[:1])
  print('true barrel core v frame truss',th,cp(blank,[q for q in f if 'truss' in q[0] or 'pillar' in q[0]])[:2])
  print('own gearmotor and revised tail at test yaw',th,cp(m,rotate(ownt,-15+30*th/105))[:1])
  print('station inserts v heel/rigid shoes at sequence',th,cp(seat,[trans(q,s*U(a)-h*X) for a in AZ for q in jaw(a) if 'heel' in q[0] or 'Take58' in q[0]])[:2])
 # Real lip test on inscribed sector away from aperture; actual upper shoe edges.
 ll=[]
 for a in AZ:
  for o in range(-60,60,5):
   for l,h in ((-7.12,-3.61),(-.27,0),(-3.61,-.27)):
    if l==-3.61 and -20<=o<=15:continue
    ll.append(washer('solid lip '+str((a,o,l)),(O+l,O+h),(14.5+.28*l,14.5+.28*h),(15.73,15.73),a+o,a+o+5,True))
 for a in AZ[:1]:
  # Inscribed material annuli for rigid front and moving shoulder; don't
  # treat a solid cylinder reserve as a real spring or a pilot bore.
  az=a;co=18.65*U(az)
  aa=[trans(v,co) for v in inner_ring('front fixed metal seat ', -.85,-.35,2.14,4.15,24)]
  bb=[trans(v,co) for v in inner_ring('heel metal seat ', -2.43,-2.03,2.14,4.13,24)]
  print('separate axial front seat vs intact wall',cp(aa,ll)[:2])
  print('front seat vs rounded shoe, remove .12 from inner radius for blend',cp(aa,[jaw(a)[0]])[:2])
  print('rear seat vs own shoe: intentional rigid integration',cp(bb,[jaw(a)[0]])[:1])
  print('fixed lip vs shoe axially displaced forward/backward',cp(ll,shift([jaw(a)[0]],.132))[:1],cp(ll,shift([jaw(a)[0]],-.12))[:1])
 print('central spine vs moving annulus key frame near park',cp(flat,shift([q for q in lip() if 'toe' in q[0] or 'cheek' in q[0]],-TR))[:2])
 print('motor v own hinge + forks',cp(m,j+shift(flange()[5:],-P))[:2])
if __name__=='__main__':grip();witnesses()
