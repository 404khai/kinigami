"""World-mm envelopes for a series draw carriage and a positive Y plug screw."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('side-package-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def xtrain(cx,back,stroke,ym=0,z=0):
    # x-moving antirotated screw / stationary thrust-bearing rotating nut.
    # x datum for the front end of the nut stack: clearance to moving socket.
    front=back-1.75; shoulder=front-.30; rear=front-3.70
    ix=rear+1.76;ic=(ym-5.50,z)
    fix=[cy('X rotary pressure nut OD',0,(rear-.55,front),(ym,z),2.50),
         cy('X forward angular race',0,(front-1.02,front+.04),(ym,z),3.80),
         cy('X rear angular race',0,(rear-.70,rear+.64),(ym,z),3.80),
         cy('X eight station index blank',0,(ix-.78,ix+.55),(ym,z),5.34),
         cy('X index locking disc',0,(ix-.78,ix+.55),ic,2.06),
         cy('X index crank plate',0,(ix+.72,ix+1.39),ic,2.90),
         cy('X crank shaft',0,(ix-3.38,ix+2.50),ic,.96),
         cy('X index input bush',0,(ix-2.57,ix-1.28),ic,2.0),
         cy('X index outer bush',0,(ix+1.5,ix+2.40),ic,2.0)]
    # Bevel at 90 degrees drives a parallel-axis Y spur pair. The thin
    # pinion quill is separately supported; do not react mesh on motor shaft.
    cr=ix-2.90;by=ym-5.5
    fix += [cy('X bevel on index shaft',0,(cr-.88,cr+.02),ic,2.35),
            cy('X bevel on Y jackshaft',1,(by-2.38,by-1.48),(cr+1.58,z),2.35),
            cy('X jackshaft',1,(-16.10,by-1.46),(cr+1.58,z),.88),
            cy('X jackshaft support',1,(-14.43,-13.62),(cr+1.58,z),1.72),
            cy('X 32T on jackshaft',1,(-16.06,-15.11),(cr+1.58,z),4.24)]
    mx=cr+1.58+3.75;mz=z+5
    fix += [cy('X gearmotor',1,(-12.92,19.88),(mx,mz),3.0),
            cy('X output pinion quill',1,(-17.48,-12.96),(mx,mz),.75),
            cy('X quill inner bearing',1,(-14.67,-13.75),(mx,mz),1.72),
            cy('X quill outer bearing',1,(-17.62,-16.63),(mx,mz),1.72),
            cy('X 18T input',1,(-16.06,-15.11),(mx,mz),2.46),
            bx('X stationary thrust bracket',(rear-.80,front+.05),(ym-4.88,ym-3.58),(z-3.6,z+3.6))]
    for sg in (-1,1):
        fix.append(bx('X race stay'+str(sg),(rear-.80,front+.10),(ym+sg*3.36-.55,ym+sg*3.36+.55),(z-3.38,z+3.28)))
    # Plunger extends THROUGH the rotating nut. Rear tip must clear hinge.
    mov=[cy('X permanently threaded plunger',0,(rear-stroke-.75,back+1.15),(ym,z),1.50),
         bx('X rear socket',(back-1.26,back+1.22),(ym-2.30,ym+2.30),(z-2.55,z+2.55)),
         cy('X crosspin',1,(ym-2.55,ym+2.55),(back+.22,z),.94)]
    # Route transverse jackshaft on +Y, away from the plug magazine.
    def mirrorY(s):
        n,v,r,d=s
        return sol(n,np.array(v)*[1,-1,1],r,None if d is None else np.array(d)*[1,-1,1])
    fix=[mirrorY(s) for s in fix]
    # Finite pin and full-revolution pin sweep, opposed-race housing to fixed
    # face crossbar, rail bolt pads. Gear and race ODs are occupancy envelopes.
    fix += [cy('X pin swept bound',0,(ix-.70,ix+.78),(ym+5.5,z),5.5*sin(pi/8)+.35),
            rod('X race frame diagonal',(rear+.3,3.75,-2.88),(13.4,8.42,-14.9),1.08),
            rod('X race frame negative',(rear+.3,-3.75,-2.88),(13.4,-8.42,-14.9),1.08)]
    L=5.50
    for sg in (-1,1):
        y=ym+sg*8.0;xc=back-2.5
        fix += [bx('X fixed wide short rail'+str(sg),(xc-L/2-.74,xc+stroke+L/2+.74),(y-.68,y+.68),(-3.84,-2.56))]
        fix += [rod('X rail bolt foot'+str(sg),(back+.4,y,-3.77),(13.4,y,-14.90),.84)]
        for k in (-1,1):
            xp=xc+k*L/2
            for h in (-1.,1.):
                mov.append(bx('X slide shoe'+str((sg,k,h)),(xp-.48,xp+.48),(y-.97,y+.97),tuple(sorted((h*.71-3.20,h*1.53-3.20)))))
        mov += [bx('X shoe socket cheek'+str(sg),(xc-3.25,back+.30),tuple(sorted((y+sg*.78,y+sg*1.50))),(-4.78,-1.62)),
                bx('X yoke lobe'+str(sg),(back-.74,back+.30),tuple(sorted((y+sg*1.4,sg*5.7))),(-4.1,.9))]
    return fix,mov
def ytrain(cx,back,ystart,stroke,pluglength):
    # moving parallel Y screw on the negative-X side of the closed track.
    rear=ystart-pluglength;nc=rear-.68;front=nc+stroke+2.28
    sx=back-3.52;z=0;end=nc-2.12
    rs=[cy('Y M3 active screw',1,(end,front),(sx,z),1.50),
        cy('Y remote radial bush',1,(front-.22,front+.87),(sx,z),2.15),
        cy('Y thrust doublet',1,(end-1.94,end-.1),(sx,z),2.84),
        cy('Y index blank',1,(end-3.61,end-2.32),(sx,z),5.34),
        cy('Y index crank pin driver',1,(end-3.61,end-2.32),(sx,z-5.5),2.06),
        cy('Y crank plate',1,(end-2.16,end-1.48),(sx,z-5.5),2.90),
        cy('Y crank shaft',1,(end-5.37,end+.23),(sx,z-5.5),.94),
        cy('Y input shaft bearing',1,(end-5.23,end-4.16),(sx,z-5.5),1.70),
        cy('Y second bearing',1,(end-.95,end+.06),(sx,z-5.5),1.70)]
    # Carry motor on X carriage. The coupled load envelope is bounded by
    # motor speed/torque and shaft support, not a locking helix.
    mx=sx+3.75;mz=z-10.50;gy=end-5.86
    rs += [cy('Y 32T',1,(gy-.52,gy+.43),(sx,z-5.5),4.24),
           cy('Y motor pinion',1,(gy-.52,gy+.43),(mx,mz),2.46),
           cy('Y gearmotor',1,(gy+2.92,gy+35.72),(mx,mz),3.0),
           cy('Y pinion quill',1,(gy-2.12,gy+2.74),(mx,mz),.74),
           cy('Y near quill bush',1,(gy+.84,gy+1.79),(mx,mz),1.74),
           cy('Y outboard quill bush',1,(gy-2.26,gy-1.19),(mx,mz),1.74),
           bx('Y thrust mounting tang',(sx-2.88,sx-1.77),(end-2.06,end+1.74),(-2.64,2.64)),
           bx('Y magazine shoe spine',(sx-2.74,back+.42),(end+.48,end+1.68),(-2.1,2.1))]
    rs += [cy('Y screw rear journal',1,(end-3.73,end+.02),(sx,z),1.12),
           cy('Y screw front journal',1,(front-.24,front+.88),(sx,z),1.14),
           cy('Y index pin swept bound',1,(end-3.50,end-2.10),(sx,z-5.5),5.5*sin(pi/8)+.35),
           rod('Y input support rib',(sx,end-.50,z-5.5),(sx-2.30,end-.56,z-1.70),.84),
           rod('Y can saddle rib',(mx,gy+3.74,mz+2.50),(sx-2.22,end-.48,z-1.78),1.1),
           rod('Y gallery lower runner',(back-.62,end+.95,-1.65),(cx-1.62,-4.2,-3.88),1.04),
           rod('Y gallery upper runner',(back-.62,end+.95,1.65),(cx-3.56,-4.2,2.55),.86)]
    mover=[cy('Y full-form nut',1,(nc-1.65,nc+1.65),(sx,z),2.22),
           bx('plug rear crossarm',(sx-.83,cx+.53),(nc-.62,nc+.67),(-1.53,1.53)),
           bx('plug key and toe',(cx-1.50,cx+1.50),(rear-1.12,rear+.47),(-1.48,1.48))]
    return rs,mover
