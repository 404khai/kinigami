"""Take 19 rear deck, independent exploratory section; Python 3 stdlib. mm/N/N mm."""
from math import cos, dist, hypot, pi, sqrt
from itertools import product

A=(.60,-4.60)                       # head axis (y,z)
M=((-6.30,15.65),(6.30,15.65))     # gearbox face at x4.0; output points aft
z=15.65-sqrt(6.9**2-2.5**2)
I=((-3.80,z),(3.80,z))
E=(-5.60,z-sqrt(8.25**2-1.8**2))
J=(9.40,z-sqrt(8.25**2-5.6**2))
S=9.30
SJ=6.00
def corners(lo,hi):return list(product(*zip(lo,hi)))
def boxes():
    b={}
    for i,m in enumerate(M):
        b['roof'+str(i)]=((3.70,m[0]-6.35,m[1]-5.35),(30.00,m[0]+6.35,m[1]+5.35))
    b['cell padded']=((1.80,-17.05,-10.55),(32.85,-11.25,10.55))
    b['head box']=((1.8,-12.70,-12.0),(34.4,12.7,12.0))
    b['tail box']=((-9.4,-12.70,-12.0),(-1.8,12.7,12.0))
    b['head panel']=((34.4,-11.9,-11.2),(35.6,11.9,11.2))
    b['tail panel']=((-10.6,-11.9,-11.2),(-9.4,11.9,11.2))
    return b
def rad(c,include_old=True):
    b=boxes()
    rs={k:max(dist(c,p) for p in corners(*v)) for k,v in b.items()
        if include_old or k.startswith(('roof','cell'))}
    rs['tail B3.215']=dist(c,(-16.078427,.60,-4.60))+3.215
    rs['untrimmed shaft caps']=max(hypot(c[0]+6.35,dist(c[1:],p)+1.85) for p in M)
    return rs
def normal_thread(lead):
    r=1.5;k=lead/(2*pi*r);mu=.23/cos(pi/6)
    return r*(k+mu)/(1-mu*k),r*(mu-k)/(1+mu*k)
def box_overlap(lo,hi,bl,bh):return tuple(round(min(a,b)-max(c,d),3) for a,b,c,d in zip(hi,bh,lo,bl))
def main():
    print("RESULT exploratory; rear drive only. E,J,I =",E,J,I)
    for m,i,o in zip(M,I,(E,J)):
        print("gear centre distances previous/next",dist(m,i),dist(i,o))
        assert abs(dist(m,i)-6.90)<1e-9 and abs(dist(i,o)-8.25)<1e-9
    print("idler-to-idler rim gap, output wheel rim gap",dist(*I)-2*3.30,dist(E,J)-2*5.55)
    print("E and J housing radial gap",dist(E,J)-2*5.4)
    # Segment distance to axis for a linear transfer arm, round section.
    def line(p,q,v):
        d=tuple(y-x for x,y in zip(p,q))
        u=max(0,min(1,sum(a*(b-c) for a,b,c in zip(d,v,p))/sum(a*a for a in d)))
        return dist(v,tuple(c+u*a for c,a in zip(p,d)))
    # J yoke = round beam crossing at z2.6, then short rise to J on +y.
    print("J yoke nearest E screw-axis (less bore/arm stock)",line((-1.5,2.6),(8.4,2.6),E)-1.1-1.55)
    print("J yoke clear E moving nut? centre distance less both radii",
          line((-1.5,2.6),(8.4,2.6),E)-1.1-2.75)
    # Same-y condition need not use entire rectangular box of the sloping E arm.
    print("E arm at J left edge along axis",E[1]+(-1.5-E[0])/(A[0]-E[0])*(A[1]-E[1]))
    joint=((3.08,5.35,-9.85),(9.32,11.50,8.85))
    # Positive cylinder penetration witness, not box overlap alone.
    w=(8.,J[0],J[1]+4.5)
    print("J rear thrust R2.5..5.0 witness in old joint motor",w,
          all(l<a<h for a,l,h in zip(w,*joint)))
    for name,axis in (("E",E),("J",J)):
        print("old-joint overlaps stationary housing stockbox",name,box_overlap(
            (3.35,axis[0]-5.4,axis[1]-5.4),(15.0,axis[0]+5.4,axis[1]+5.4),*joint))
    print("true worst E thrust housing to relocated padded cell (y)",E[0]-5.4-(-11.25))
    for name,n0,n1,ss in (('E',16.45,19.45,S),('J',16.45,19.45,SJ)):
        print(name,"nut sweep / min thread-end reserves",n0,n1+ss,n0-16.15,29.20-n1-ss)
    print("E piston rest/forward; initial ball gap; end past full nose advanced .25",30.90,30.90+S,31.535-30.90,30.90+S-(39.137+.25))
    print("terminal wire span/after .25 cage advance (not flex-zone rating)",29.10-16.0,29.35-16.0)
    print("E crossbar forward minus cage rear clearance",27.20-(17.55+S))
    # Slot in raised rim of divided piston, not a through slot in the stud.
    print("twin runner to .90 beam after .08 drift",1.1-.425-.45-.08)
    print("wider bore at piston aft rim minus drift/profile/Rmax",3.87+.42*(30.90-.55-34.90)-.04-.05-1.78)
    print("wire nominal tension stress at 45N",45/(pi*.4**2/4))
    print("crossbar nominal bend 45N, simple span 8.4, .9x2.8",6*45*8.4/4/(.90*2.80**2))
    # Conservative sufficient upper estimates for two longitudinal guide
    # support lines, nominal dry; absent preload/seizure, quasi-static only.
    eta=.85;mu=.23; L=10.
    for lab,o,Ld,Fout,earm,point in (("draw",E,2.,45.,.15,.59),("eject one post",E,2.,8.,6.8,.59),
                                     ("jaw",J,1.,30*(1+mu)/(1-mu),6.8,1.)):
        C,Cl=normal_thread(Ld)
        # screw torque reacted through a separate anti-rotation couple at effective R5.
        g=2*mu*dist(o,A)/L+mu*C/5
        f=Fout*(1+2*mu*earm/L)/(1-g)
        # Unequal guide friction can act as far as 5 mm off centre.
        p=2*mu*5/L
        fc=Fout*(1-p+2*mu*earm/L)/(1-p-g)
        T=C*f+3
        print(lab,"guide feedback / screw thrust / nut torque / available at moving point",
              g,f,T,point*98.0665*35/26*eta, "off-centre friction torque",C*fc+3)
    c=(10.51919432,-.04952138,1.31213911)
    print("diameters about",c,[(k,round(2*r,3)) for k,r in rad(c).items()])
    # For any centre k, weighted squared distance to k is at least the
    # variance about the weighted mean. All weights positive; no optimizer.
    ball=(-16.078427,.6,-4.6)
    w=(.30759926,.26060206,.01875103,.41304765)
    pts=((30,12.65,21),(32.85,-17.05,-10.55),(35.6,11.9,-11.2),
         tuple(b+3.215*(b-v)/dist(ball,c) for b,v in zip(ball,c)))
    mean=tuple(sum(q*r[i] for q,r in zip(w,pts)) for i in range(3))
    lb=2*sqrt(sum(q*dist(r,mean)**2 for q,r in zip(w,pts)))
    print("axis-independent lower bound for specified four stock points incl tail ball",lb)
    assert abs(sum(w)-1)<1e-9 and lb>60
    assert min(31.535-30.90,27.20-17.55-S,29.2-19.45-S)>0

if __name__=='__main__':main()
