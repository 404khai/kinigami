"""Adverse equilibrium of the *first-order* clearance coupling, not a jam test.

All force vectors act on the stud-side member. We normalize the reaction at
one jaw to 1 N axial. Witness initially found by linear programming with an
INSCRIBED 12-ray cone; this verifier needs only Python's standard library.
Axes x axial, yz transverse; points in mm, rotations in rad.
"""
from math import cos, dist, pi, sin, sqrt


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def cross(a, b):
    x,y,z=a; u,v,w=b
    return (y*w-z*v,z*u-x*w,x*v-y*u)


def contacts():
    for j in range(3):
        angle=2*pi*j/3
        centre=(0,5.35*cos(angle),5.35*sin(angle))
        for h in (1,-1):
            n=tuple(x/sqrt(2) for x in (1,-h*sin(angle),h*cos(angle)))
            p=tuple(c-1.4*a for c,a in zip(centre,n))
            yield p,n,.010/sqrt(2)
    yield (.12,-.74,0),(-1,0,0),.010


if __name__ == "__main__":
    q=(.0176485788,0,.0552971576,.00516795866,0,-.0103359173)
    forces=((0,0,0),
            (.25067673952,.00745866299,-.19796278014),
            (.22939912770,-.22786321438,-.06412759092),
            (.12400609731,.09160903108,.08934069836),
            (.29537670385,.20307004529,-.07968573955),
            (.10054133162,-.07427452499,.07243541226),
            (-1,0,.18))
    all_forces=[]; all_moments=[]
    for i,((p,n,g0),f) in enumerate(zip(contacts(),forces)):
        g = g0+dot(n,q[:3])+dot(cross(p,n),q[3:])
        fn=dot(f,n)
        ft=dist(f,tuple(fn*a for a in n))
        assert fn >= 0 and ft <= .180001*fn
        assert (i==0 and g>.117) or (i!=0 and abs(g)<1e-8)
        print(f"contact {i}: gap {g:.6f}, N {fn:.6f}, |T|/N {ft/fn if fn else 0:.6f}")
        all_forces.append(f); all_moments.append(cross(p,f))
    for name,rows in (("force",all_forces),("moment",all_moments)):
        residual=max(abs(sum(values)) for values in zip(*rows))
        assert residual<1e-8
        print(f"{name} max component residual {residual:.3e}")
