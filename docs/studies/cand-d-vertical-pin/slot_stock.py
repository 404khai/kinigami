"""Finite guide-window walls, material vs registered ring and boss clearances."""
from math import pi
import numpy as np
from button_seats import setup


def parts(offset=12.,lower=1.,upper=19.):
    xp=12.3898; R=2.; half=.85; slot=R+.035
    for j,(y,z,k) in enumerate(((-8,lower,0),(8,lower,0),(0,upper,0),(0,lower,1),(8,upper,1))):
        c=np.array([xp-offset,y,z]); n=np.eye(3)[k]; a=np.eye(3)[1-k]; v=np.eye(3)[2]
        # One-piece window, two parallel running walls plus closed end bars;
        # full moving stroke swept vertically while the torus stays at home.
        for s in (-1,1):
            cc=c+s*(slot+.65)*n-6.35*v
            h=.65*n+(half+.20)*a+(6.35+R+.30)*v
            yield f'{j+1} wall {s}',cc-h,cc+h+12.7*v
            cc=c+(s*(6.35+R+.30+.65)-6.35)*v
            h=(slot+1.30)*n+(half+.20)*a+.65*v
            yield f'{j+1} cap {s}',cc-h,cc+h+12.7*v


def clear(points,lo,hi):
    return np.linalg.norm(np.maximum(lo-points,np.maximum(points-hi,0)),axis=1)


def check(offset,lower,upper):
    u=np.arange(4096)*2*pi/4096
    ring=np.column_stack((15+7.5*np.cos(u),7.5*np.sin(u),np.zeros_like(u)))
    boss=setup(-90,11.,6.,58.)[3][::2]
    return min((min(min(clear(ring,lo,hi))-7.5*pi/len(u),
                    min(clear(boss,lo,hi)))-4.2,label)
               for label,lo,hi in parts(offset,lower,upper))


def moving_slots():
    # One Y guide rail for BOTH roller rows; keep its end caps outside both
    # full strokes. The three X-normal axles each need one separate slot.
    # Stud axes of the X followers point OUT of their window and the Y
    # studs face rearwards. Only cross-pair roller bodies/shafts checked.
    xp=.3898
    defs=[(-10.,-4.,-4.,0),(10.,-4.,-4.,0),(0.,8.,8.,0),(5.,-4.,8.,1)]
    boxes=[]
    rollers=[]
    for j,(y,z,b,k) in enumerate(defs):
        n=np.eye(3)[k]; a=np.eye(3)[1-k]; v=np.eye(3)[2]
        C=np.array([xp,y,(z+b+12.7)/2]); h=(b+12.7-z)/2+2.30
        for s in (-1,1):
            cc=C+s*2.685*n
            spread=.65*n+1.05*a+h*v
            boxes.append((j,cc-spread,cc+spread))
            cc=C+s*(h+.65)*v
            spread=3.335*n+1.05*a+.65*v
            boxes.append((j,cc-spread,cc+spread))
        direction=-1 if j!=1 else 1
        for h in sorted({z,b}):
            C=np.array([xp,y,h])
            # Enclosing boxes (not material witnesses when overlapping).
            for L,R,f in ((.85,2.,0.),(2.65,1.95,direction*3.50)):
                cc=C+f*a
                lo=cc-L*a-R*(n+v); hi=cc+L*a+R*(n+v)+12.7*v
                rollers.append((j,lo,hi))
    boss=setup(-90,11.,6.,58.)[3][::2]
    u=np.arange(4096)*2*pi/4096
    ring=np.column_stack((15+7.5*np.cos(u),7.5*np.sin(u),np.zeros_like(u)))
    def sep(A,B):
        return np.linalg.norm(np.maximum(A[1]-B[2],np.maximum(B[1]-A[2],0)))
    print('fixed slot walls / nonown roller+stud swept box gap',
          min(sep(a,b) for a in boxes for b in rollers if a[0]!=b[0]))
    print('nonown fixed slot stocks minimum gap',
          min(sep(a,b) for a in boxes for b in boxes if a[0]!=b[0]))
    print('fixed slot or moving roller/stud / seated eye and boss lower clearance',
          min(min(min(clear(ring,a,b))-7.5*pi/len(u),min(clear(boss,a,b)))-4.2
              for j,a,b in boxes+rollers))
    return boxes,rollers


if __name__=='__main__':
    moving_slots()
    for off in (6.,9.,12.,15.):
        for z in (1.,4.):
            print('offset, bottom, tallest axle, sweep bound + limiting wall',
                  off,z,z+18.,check(off,z,z+18.))
