"""Analytic tube-wall and mechanism audit, not a simulation or acceptance run."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('bore-install-take53.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
magR=5.48;mx=8.6;my=-6-magR;mz=-2*Rp
def magpts():
    t=np.linspace(.01,pi-.01,361)[:,None]
    center=np.column_stack((mx+magR*np.sin(t),my+magR*np.cos(t),np.zeros(len(t))+mz))
    n=np.column_stack((np.sin(t),np.cos(t),np.zeros(len(t))))
    ph=np.arange(180)*pi/90
    return (center[:,None,:]+2.07*(np.cos(ph)[None,:,None]*n[:,None,:]+np.sin(ph)[None,:,None]*np.array([0,0,1]))).reshape(-1,3)
def trj(v,a,o):
    m=np.array([[cos(a),-sin(a),0],[sin(a),cos(a),0],[0,0,1]])
    return (v-o)@m.T+o
def adjwall(up,down,yaw,u=0,v=0,gap=0):
    # A point on the upstream BEND wall. Seek same material in downstream
    # RETURN STRAIGHT. Far from ends or turn in second magazine.
    p=trj(magpts(),radians(up),A)-[u,0,0]
    q=trj(trj(p-[P+gap,0,0],-radians(yaw),H)+[v,0,0],-radians(down),A)
    rho=np.hypot(q[:,1]-(my-magR),q[:,2]-mz)
    dist=np.min(np.array([rho-1.90,2.24-rho,q[:,0]+16,mx-q[:,0],np.repeat(.17,len(q))]),axis=0)
    k=dist.argmax();return round(dist[k],6),sh(p[k]),sh(q[k])
def strand_checks():
    # Enclose every nominal straight head strand by a convex prism inflated
    # with max bead radius. Discontinuous tail contacts beyond F not excluded.
    fx=fixed()+additions()+[sol(s[0],s[1]+trans(s,[-ST,0,0])[1],s[2],s[3]) for s in trunk()+feedmotor()]+eboard()+splitguide(3.3)+shutter(0)+blinds(False)+outriggers()
    for sg in (-1,1):
        cen=6*sg;line=bx('strand envelope',(A[0]-ST-R*sin(YMAX)-.2,F),(cen-.63,cen+.63),(-.63,.63))
        ls=sol(line[0],line[1],1.25)
        vv=sorted([(*pairs([ls],[s]),) for s in fx])
        print('strand fixed broad screen',sg,vv[:4])
def main():
    print('world U centreline apex X; knuckle at H R3.10',F-P+LEG+R,H)
    w=np.array([-8.52,0,0]);dt=w[0]-(F-P+LEG+R);dk=abs(w[0]-H[0])
    print('knuckle/U common point; distance to U centreline, hinge axis / common radial ball for knuckle bore<=2.35 and B1.45/B1.65',w,dt,dk,[min(dt-b,b+W-dt,dk-2.35,3.10-dk) for b in (1.45,1.65)])
    for yaw in (0,-10,-15,15):
        for up,down,u,v,gap in [(0,0,0,0,0),(0,0,0,0,1.55),(17,0,0,0,0),(-17,17,2.4,.6,0),(17,-17,.6,.6,0)]:
            print('adjacent two actual magazine walls, yaw/rock1/rock2/draw1,2/gap/witnessR,world,local2 (negative not a clearance)',yaw,up,down,u,v,gap,adjwall(up,down,yaw,u,v,gap))
    strand_checks()
    for pitch in (3.10,p,3.40):
        u=(15*pitch-(2*(F-A[0])+2*LEG+pi*R))/2
        st=20*pitch-5*pitch-(F-A[0]-3.42)
        store=(mx-A[0])+pi*magR+mx+16
        print('20-interval shoe tangent: pitch, draw u if no local compression, home shoe reach/spare',pitch,u,st,store-st)
    print('keeper outer radial gap to tooth crest; nominal tooth to next cut at midpoint, aperture growth over 5 pockets at p3.40',1.40-1.02,2*Rp*sin(pi/(2*N))-1.37,5*(3.40-p))
    print('approx hollow U shell g (no mouth, fins or flanges), magazine wall g, inertial torque per g-mm at 1g',pi*((1.65+W)**2-1.65**2)*(2*LEG+pi*R)*.0079,pi*(2.24**2-1.90**2)*((mx-A[0])+pi*magR+mx+16)*.0079,.00980665)
    print('outreach of sharp fork vs local face / parked tip-face and blind back clearance',F-(A[0]+1.34+R*sin(YMAX)),3.42-1.25,3.42-1.25-1.77)
    for L in (3.50,2.90):
        for mu in (.02,.05,.10,.15):
            den=1-2*mu*13.65/L
            print('eccentric guide ideal opposed contact lever / mu / thrust ratio and gearhead torque F55.5 and113', L,mu, 'self-binding not excluded' if den<=0 else [round(k,3) for k in [(1+2*mu*10.25/L/den)*f for f in (1.,55.5*.5/(2*pi*.28*32/18*.75),113*.5/(2*pi*.28*32/18*.75))]])
    for l in (3.,6.):
        print('stripper axial tilt moment if one ring jammed at R6 / guide couple at 4.4mm',l*6,l*6/4.4)
    for rate,eff,length in [(16,.80,26.9),(64,.70,29.6),(256,.60,32.3)]:
        print('0615 3V rated * gearbox MAX efficiency, ratio, gear output Nmm (cap25), length',rate,min(25,.156*rate*eff),length)
if __name__=='__main__':main()
