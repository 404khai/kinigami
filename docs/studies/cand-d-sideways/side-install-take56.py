"""Exploratory side discharge installation; analytic circles govern lip contact."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('side-drive-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import sys
sys.path.insert(0,str(D.parent/'cand-d-lace'))
import twin_crowns as cr
RB=3.50;RI=3.65;RO=5.65;SL=1.65;XC=sqrt(RO**2-SL**2);rho=sqrt(RI**2-SL**2)-sqrt(RB**2-SL**2)
S=19.54-6.;CX=S-rho;BACK=CX-RO;DX=3.625;DY=9.625;Y0=-4.0;PL=9.95
def clip(p,j,b,sg):
    q=[]
    for c,e in zip(p,p[1:]+p[:1]):
        aa=(c[j]-b)*sg;bb=(e[j]-b)*sg
        if aa>=0:q.append(c)
        if aa*bb<0:q.append(c+(e-c)*aa/(aa-bb))
    return q
def shell(y0,y1,prefix,inside=False,ro=RO):
    out=[];count=48;a=pi/count
    ri=RI/cos(a) if inside else RI;rr=ro if inside else ro/cos(a)
    for i in range(count):
        angles=[i*2*a,(i+1)*2*a]
        poly=[r*np.array([cos(t),sin(t)]) for r,t in [(ri,angles[0]),(rr,angles[0]),(rr,angles[1]),(ri,angles[1])]]
        for k,rules in enumerate([[(0,0,-1)],[(0,0,1),(1,SL,1)],[(0,0,1),(1,-SL,-1)]]):
            q=clip(poly,0,XC,-1)
            for j,b,sg in rules:q=clip(q,j,b,sg)
            if prefix.startswith(('gallery','Gt')):
                q=clip(q,1,3.38,-1)
                # Open a rear crossarm slot at -X only in the gallery.
                if k==0:
                    for sg in (-1,1):
                        z=clip(q,1,sg*1.66,sg)
                        if len(z)>2 and abs(sum(u[0]*v[1]-u[1]*v[0] for u,v in zip(z,z[1:]+z[:1])))>1e-8:
                            out.append(sol(prefix+str((i,k,sg)),[(CX+x,y,w) for x,w in z for y in (y0,y1)]))
                    continue
            if len(q)>2 and abs(sum(u[0]*v[1]-u[1]*v[0] for u,v in zip(q,q[1:]+q[:1])))>1e-8:
                out.append(sol(prefix+str((i,k)),[(CX+x,y,z) for x,z in q for y in (y0,y1)]))
    return out
def keyplug():
    return [cy('plug cylindrical core',1,(Y0-PL,Y0),(CX,0),RI-.10),
            bx('plug slit tongue',(CX,CX+XC),(Y0-PL,Y0-1.50),(-1.55,1.55))]
def face():return [sol(s[0],s[1],s[2],s[3]) for s in cr.stock()[0]+cr.frame()]
def mated():
    t=[sol(s[0],s[1],s[2],s[3]) for s in cr.stock()[1]]
    t += [sol('ball',[(S,0,0)],RB),cy('neck',0,(S,19.54),(0,0),1.50),cy('shoulder',0,(19.54,21.54),(0.,0.),2.80),
          cy('tail core',0,(21.26,24.14),(0.,0.),1.84)]
    for j in range(3):
        y=13*cos(radians(-90+120*j));z=13*sin(radians(-90+120*j))
        t += [cy('crown pier'+str(j),0,(19.42,21.22),(y,z),1.46),rod('crown stay'+str(j),(21.22,y,z),(22.36,0,0),1.32)]
    for k in (-1,1):
        t += [rod('tail fork'+str(k),(23.64,0,k*.85),(P-11.,0,k*6.15),1.45)]
    t +=shift([s for s in V['own_tail_straight'] if s[0].startswith(('tail pivot lug','sector web','tail sector hub','fork tip'))],P)
    return t
def parts():
    xf,xm=xtrain(CX,BACK,DX);ys,ym=ytrain(CX,BACK,Y0,DY,PL)
    fix=[sol(*s) for s in V['joint']]+face()+pads()+xf
    mov=xm+ys+shell(-4,4,'C shell tile')+shell(Y0-PL-.16,-4,'gallery tile',ro=4.75)
    mov += [bx('axial rear yoke',(BACK-1.14,BACK+.42),(-6.86,6.86),(-1.58,1.58)),
            bx('gallery transfer tie',(BACK-.94,CX-3.82),(-11.22,-9.85),(-1.43,1.43)),
            bx('X load cell bridge reserve',(BACK-2.70,BACK-.82),(-2.55,2.55),(-1.48,1.48))]
    # Captured preload stack/guide and switches reserved below load path; no
    # overload force rating asserted from their envelopes alone.
    fix += [bx('X load ADC and switch',(-.80,3.10),(3.80,6.72),(-4.50,-2.60)),
            bx('X dwell flags',(-2.45,.80),(-8.4,-6.05),(-4.10,-2.00)),
            bx('X overload quill reserve',(-.92,1.25),(-7.92,-5.67),(-2.74,-.84))]
    mov += [bx('Y draw overrun pickup',(BACK-5.72,BACK-3.25),(-12.12,-8.82),(2.92,4.38)),
            bx('Y parked/retracted key sensor',(BACK-3.8,BACK-.95),(-4.85,-2.70),(2.82,4.62))]
    return fix,mov,keyplug()+ym,shift(mated(),-P)
def efind():
    f,m,y,t=parts();q=boxesweep(reduce(m),[DX,0,0])+boxesweep(boxesweep(y,[0,DY,0]),[DX,0,0])
    rt=[s for j in np.linspace(-15,15,13) for s in reduce(rotate(t,j))]
    # Hausdorff yaw grid error for <=24mm own-tail sweep radius about H.
    rec=elec(reduce(f)+q+[sol(s[0],s[1],s[2]+.34,None if s[3] is None else None) for s in rt])
    (D/'side-boards-take56.json').write_text(json.dumps(rec,separators=(',',':'))+'\n')
def stock():return json.loads((D/'side-boards-take56.json').read_text())
def meshcap(a,b):
    ea=extlist(a);eb=extlist(b);best=[]
    for i,s in enumerate(a):
        G=np.maximum(ea[i,0]-eb[:,1],eb[:,0]-ea[i,1]).max(1)
        for j in np.flatnonzero(G<-.01):
            t=b[j];w=ball(s,t)
            if w[3]>.005:best.append((round(float(w[3]),5),s[0],t[0],tuple(round(v,5) for v in w[:3])))
    return sorted(best,reverse=True)
def runs():
    f,m,y,t=parts();e=stock();ff=face();tail=mated();h=cr.stock()[0];tc=cr.stock()[1]
    print('datums Cx, seated ball centre, rear X, clip front, neck tip',CX,S,BACK,CX+XC,S+6)
    print('straight/index and parked filled proxy enclosures',enc(f+m+y+t+e),enc(f+m+shift(y,0,DY)+t+e))
    print('parked filled after reverse X, own straight',enc(f+shift(m,DX)+shift(y,DX,DY)+t+e))
    print('floor',min(ext(s,np.eye(3))[0][2] for s in f+m+y+t+e))
    sets={'fixed':f,'x_carriage':m,'x_and_y_plug':y,'straight_own_tail':t,'boards':e}
    (D/'side-model-take56.json').write_text(json.dumps(dict(units='mm',pitch=P,H=sh(H),ball=[S,0,0],C=[CX,0,0],dx=DX,dy=DY,groups=sets),separators=(',',':'))+'\n')
    v=[*meshcap([s for s in m if s[0] in ('Y gearmotor','X permanently threaded plunger','Y 32T')],ff+f[:len(V['joint'])]+t)]
    print('positive occupied ball at service (claims on cans, frame, screw core reviewed separately)',v[:12])
    c=shell(-4,4,'Ct',True)+shell(Y0-PL-.16,-4,'Gt',True,ro=4.75)
    for q in (0,DX):
        print('actual track/gallery vs finite frame at q',q,meshcap(shift(c,q),cr.frame())[:3])
    # Compare swept electronics and fixtures against actual adjacent head in
    # aligned stow, during lift if held, and in conditional lateral motion.
    left=reduce(f+m+y+e);adj=reduce(f+m+y+e);rt=rotate(t,0)
    for name,q,yo,neighborx,neighbory in [('mated',0,0,0,0),('held lift',DX,0,0,0),('held discharge',DX,DY,0,0),('following lateral',DX,DY,DX-(rho+.15),Y0+DY+RB)]:
        left=reduce(f+e+shift(m,q)+shift(y,q,yo))
        v=[(*pairs(left,shift(rotate(adj,a),P+neighborx,neighbory)),a) for a in range(-15,16,3)]
        print('two-head broad/model test',name,min(v))
    # No clocked seam taken as a collision just from a broad-phase overlap.
    for a in (-15,0,15):
        aa=f+m+y+e;bb=shift(rotate([s for s in aa if s[0] in ('X gearmotor','Y gearmotor','cell','computer','Y 32T','X jackshaft','yaw gearmotor')],a),P)
        print('two-head nominal material on cans/boards at yaw',a,meshcap([s for s in aa if s[0].startswith(('side ','cap ','Y gearmotor','X gearmotor','computer','cell','top cross','lower cross'))],bb)[:3])
    fmax=max(ext(s,np.eye(3))[1][0] for s in ff);cmin=min(ext(s,np.eye(3))[0][0] for s in tc)
    lift=DX-rho-.15
    print('flat/frame max x, crowns min x / hard floor take-up / ideal following lift / full transverse slab clearance',fmax,cmin,rho+.15,lift,lift+cmin-fmax)
    print('park plug front/back, overshoot, ball Y required if stays in front; radial key recess',Y0+DY,Y0+DY-PL,Y0+DY-4,Y0+DY+RB,0.0)
    print('park key front / rear',Y0+DY-1.50,Y0+DY-PL)
    print('X plunger axis positions and hinge',next(s[1] for s in m if s[0]=='X permanently threaded plunger'),H)
    # Convex frame/plug identities for conditional tightly constrained paths.
    for q in (0,DX):
        pv=boxesweep(shift(y,q),[0,DY,0]);print('transverse plug+crossarm swept vs fixed face',q,pairs(pv,ff),meshcap(pv,ff)[:4])
if __name__=='__main__':
    if 'search' in sys.argv:efind()
    else:runs()
