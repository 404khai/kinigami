"""Full 3D rigid/translational support screens with independent material witnesses."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('side-install-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def mr(ls,a,cx,cy,dx=DX):
    return shift([rot(s,radians(a),np.array([S,0,0])) for s in ls],dx+cx-rho,cy)
def sweep():
    f,m,y,t=parts();e=stock();fh=face();mt=mated()
    xf,xm=xtrain(CX,BACK,DX);ys,ym=ytrain(CX,BACK,Y0,DY,PL)
    # Includes both axes full continuous translation and independent held/following
    # neighbours. Boxes for grouped stock overestimate, not understate clearance.
    head=reduce(f+e)+boxesweep(reduce(m),[DX,0,0])+boxesweep(boxesweep(reduce(y),[0,DY,0]),[DX,0,0])
    r=max(far(s,H) for s in head);debit=.20+2*r*sin(radians(.25))
    span=[]
    for a in range(-15,16):
        nn=shift(rotate(head,a),P)
        nn=boxesweep(boxesweep(nn,[DX,0,0]),[0,Y0+DY+RB,0])
        v=pairs(head,nn);span.append((*v,a))
    print('two powered heads, independent X/Y screw stroke, following/held translation box, ±15 yaw; raw gap, worst yaw, radius & total debit',min(span),r,debit,'cert',min(span)[0]-debit)
    # Cover nominal axial carriage vs face e.g. gallery throughout stroke,
    # and the solid Y paths against the fixed output (at both +X and -X).
    for desc,aa,bb in [('C/gallery vs fixed face',boxesweep(shell(-4,4,'Ct')+shell(Y0-PL-.16,-4,'Gt',ro=4.75),[DX,0,0]),fh),
                       ('plug and strut vs fixed face',boxesweep(boxesweep(y,[0,DY,0]),[DX,0,0]),fh),
                       ('Y drive vs fixed X machinery',boxesweep(ys,[DX,0,0]),xf),('X drive vs fixed hinge',xf,V['joint']),
                       ('Y motor and crossarm',ys,boxesweep(ym,[0,DY,0])),('X geared drive vs fixed head face',xf,fh)]:
        print(desc,pairs(aa,bb))
    # Check specific continuous material — boxes, threaded rod MINIMUM root,
    # full can, brackets — never identify a bored race/gear blank as solid.
    xmetal=[s for s in xf if s[0] in ('X gearmotor','X jackshaft','X crank shaft','X stationary thrust bracket') or s[0].startswith(('X fixed wide','X race stay'))]
    ymetal=[s for s in ys if s[0] in ('Y gearmotor','Y crank shaft','Y thrust mounting tang','Y magazine shoe spine','Y pinion quill')]
    studpl=next(s for s in xm if s[0]=='X permanently threaded plunger')
    src=[sol(studpl[0]+' core',studpl[1],1.18,studpl[3])]+[s for s in xm if s[0].startswith(('X shoe socket','X slide shoe'))]
    for u in (0,DX/2,DX):
        print('material: moving X, positive Y can and brackets vs fixed X',u,meshcap(shift(src+ymetal,u),xmetal)[:6])
        print('material: Y can/brackets vs own articulated tail',u,sorted([(*w,a) for a in (-15,0,15) for w in meshcap(shift(ymetal,u),rotate(t,a))],reverse=True)[:3])
    mm=shift([s for s in m if not s[0].startswith(('C shell','gallery','Y index blank','Y full-form'))],DX)
    # Check the rest of original Take55 tail; intended stud/C reactions omitted.
    local=[s for s in mt if not s[0].startswith(('ball','neck','shoulder'))]
    for lab,ang,cx,cy in [('sharp',-15.25,.169099,-.3893213),('rounded',-17.25,.172095,-.196669)]:
        position=mr(local,ang,cx,cy)
        rest=f+e+mm+shift(keyplug(),DX)
        print(lab,'pose plug advance for first tangent',cy-RB-Y0,'rest of mated tail vs fixed head, overlap proxies',pairs(position,rest))
        solids=[s for s in position if not s[0].startswith('crown') or s[0].startswith(('crown pier','crown stay'))]
        print(lab,'actual tail mounts vs unbored head',meshcap(solids,[s for s in rest if s[0].startswith(('side ','cap ','top cross','lower cross','X gearmotor','Y gearmotor','computer','cell','Y magazine shoe spine'))])[:4])
        for a in (-15,0,15):
            nn=mr(shift(rotate(head,a),P),ang,cx,cy)
            print(lab,'whole rotated neighbour head vs upstream head (outer)',a,pairs(head,nn))
        # Slab test with *actual* oriented crown & frame; positive value also
        # covers all ΔY. Negative values may still be separated in Y or Z.
        print(lab,'crown/flat X slab gap',min(ext(s,np.eye(3))[0][0] for s in position[:6])-max(ext(s,np.eye(3))[1][0] for s in fh))
    # Alternative square face goal is conditional displacement, not ability.
    fxe=max(ext(s,np.eye(3))[1][0] for s in fh)
    for ya in (0,3,6,10,15):
        orig=mt[:6];sx=DX-rho-.15
        minx=min(ext(s,np.eye(3))[0][0] for a in (-ya,ya) for s in mr(orig,a,-.15,0))
        print('genuinely following floor-contact neighbour / yaw / all-Y index slab clearance',ya,round(minx-fxe,4),'lift',sx)
def loads():
    for b in (0,3,8,15,30,45):
        print('central resultant cone / 70g inherited face service, table, illustrative fault',b,np.round(cr.budget(70,13,60,(0,0),1,port_angle=b,p=38.,x=S-17.04,clock=-90,crown_shift=8-1.85),3))
    print('one-sided lip normal angle from X & μ=.23 cone; two-symmetric lips not assumed',degrees(asin(SL/RB)),degrees(asin(SL/RB))+degrees(atan(.23)))
    # Eight-slot Geneva: R/C=sin(pi/8). During the cut interval, max output
    # angular speed / input angular speed occurs at pin closest to output.
    gc=5.5;ratio=sin(pi/8)/(1-sin(pi/8));pin=gc*sin(pi/8);lever=gc-pin
    print('8-station pin radius, minimum moment arm, speed ratio peak, dwell deg, screw increment',pin,lever,ratio,180+360/8,.5/8)
    for f in (42.,55.5,75.,113.):
        # Use .25 load-line and guide error, nominal 5.5 shoe centre span.
        s=ecc(f,.15,4.54,.25,.25);sc=s*.50/(2*pi*.28)
        print('X centered draw, screw thrust with guide, screw torque, pin reaction, motor-output torque incl geneva eff .72 and 18:32 at .75',f,s,sc,sc/lever,sc*ratio/(.72*(32/18)*.75))
    ey=CX-(BACK-3.52) # offset between screw & plug force line
    for mu in (.05,.15,.23):
        for L in (7.0,4.0):
            f=ecc(8.,mu,L,ey,ey)
            print('Y 8N stud, guide mu and contact span / eccentricity, thrust motor-output torque',mu,L,ey,f,f*.5/(2*pi*.28)*ratio/(.72*(32/18)*.75))
    for f in (55.5,113.):
        n=f/cos(asin(SL/RB));fy=f*tan(asin(SL/RB))
        print('one lip no friction first-order axial F, N and vertical / neck tension/bending over6 mm (no notch)',f,n,fy,f/(pi*1.5**2),4*fy*6/(pi*1.5**3))
    print('rigid held neighbour, interference at full reverse if no compliance',DX-(rho+.15))
if __name__=='__main__':sweep();loads()
