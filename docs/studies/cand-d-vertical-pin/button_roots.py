"""Metal backing, pressure and local fit for the selected inclined registry."""
from math import cos, hypot, pi, radians, sin, sqrt
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from button_seats import setup, X,Y,Z
from slotted import hertz


def dc(x,base,n,L,R):
    v=x-base; u=v@n; v=v-np.outer(u,n)
    return np.hypot(np.maximum(np.linalg.norm(v,axis=1)-R,0.),
                    np.maximum(np.maximum(-u,u-L),0.))


def main():
    q,c,e,ps,ns=setup(-90,11.,6.,58.); mu=.23
    # Deliberately charge the entire sum of normal load to one stem. All
    # face contacts have the same polar angle to the intended draw axis e.
    gx=cos(radians(58.6))-mu*sin(radians(58.6))
    B=5*.07*9.80665+2*.07*9.80665
    den=e[0]-np.tan(np.arctan(mu)+radians(2))*e[2]
    P=(76.+5*.07*9.80665)/den
    U=(P+B)/gx; L=4.; rho=1.20; W=pi*rho**3/4; E=200000
    A=pi*rho**2; I=W*rho; hit=hertz(U,4.2,4.2)
    # Valid only for a pole in this patch. A ball may not be allowed to load
    # a free edge and then be assigned the nominal centred Hertz ellipse.
    ecc=.55; T=mu*U; M=U*ecc+T*L
    sigma=U/A+M/W; tau=4*T/(3*A)+T*ecc/(2*W)
    tip=U*L/(A*E); side=(T*L**3/3+U*ecc*L**2/2)/(E*I)
    print('P max, all normal on one land, Hertz radius and GPa',
          *(round(x,4) for x in (P,U,hit[0],hit[-1]/1000)))
    print('Ø2.4 x 4 root axial + bending, max VM conservative MPa; axial & transverse mm',
          *(round(x,5) for x in (sigma,hypot(sigma,sqrt(3)*tau),tip,side)))
    # Lipschitz circle sampling: any unsampled core lies within R*pi/N of
    # a sampled core (arc length); distance-to-solid is 1-Lipschitz.
    u=np.arange(2048)*2*pi/2048
    ring=np.column_stack((15.+7.5*np.cos(u),7.5*np.sin(u),np.zeros_like(u)))
    stems=[]
    for j,(p,n) in enumerate(zip(ps,ns)):
        front=p-4.2*n; base=front-L*n
        rg=min(dc(ring,base,n,L,rho))-4.2-7.5*pi/len(u)
        peers=np.array([v for i,v in enumerate(ps[::2]) if i!=j//2])
        pg=min(dc(peers,base,n,L,rho))-4.2
        print(j+1,'base, torus / other ball clearance',np.round(base,3),round(rg,4),round(pg,4))
        stems.append((base,n))
    # Separation of any two finite cylinders by a support plane. A failed
    # trial axis is only inconclusive; do not label it a material witness.
    for i,(b,n) in enumerate(stems):
        for j,(c,m) in enumerate(stems[:i]):
            d=b+L*n/2-c-L*m/2
            dirs=np.array([X,Y,Z,n,m,d,np.cross(n,m),b-c])
            dirs=dirs[np.linalg.norm(dirs,axis=1)>1e-10]
            dirs=dirs/np.linalg.norm(dirs,axis=1)[:,None]
            a=dirs@n; z=dirs@m
            mx=max(abs(dirs@d)-L*(abs(a)+abs(z))/2-rho*(
                np.sqrt(np.maximum(0,1-a*a))+np.sqrt(np.maximum(0,1-z*z))))
            if mx<.2: print('inconclusive stem/stem',i+1,j+1,mx)


if __name__=='__main__':main()
