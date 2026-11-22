"""Study only: 2-principal-curvature elastic Hertz contacts (mm, N, MPa).
Half-space assumptions; not a pressure allowable or a proof of edge shape.
"""
from math import pi,sqrt
from scipy.integrate import quad
from scipy.optimize import brentq

def integrals(k):
    # Substitute t=u^2 in the normal-curvature half-space integrals;
    # a=1, b=k here. Scaling the semiaxes by a scales each integral a^-3.
    def integrand(u,major):
        A=1+u*u; B=k*k+u*u
        return 2/((B if major else A)*sqrt(A*B))
    return [quad(integrand,0,float('inf'),args=(b,),epsabs=1e-12)[0] for b in (False,True)]

def hertz(F,Rx,Ry,E=115400.):
    assert 0<Rx<=Ry and F>0
    def residual(k):
        ix,iy=integrals(k)
        return ix/iy-Ry/Rx
    k=1 if Rx==Ry else brentq(residual,1,1024)
    ix,iy=integrals(k)
    a=(3*F*Rx*ix/(2*pi*E))**(1/3)
    b=k*a
    return a,b,3*F/(2*pi*a*b)
if __name__=='__main__':
    rb=1.045
    for F in (13.54,25.28,43.1):
        for tip in (float('inf'),.1,.35,.6):
            for transverse in (rb,6.,20.):
                rx=1/(1/rb+1/tip)
                a,b,p=hertz(F,rx,transverse)
                if tip==float('inf') and transverse==rb:
                    assert abs(a-(3*F*rb/(4*115400.))**(1/3))<1e-10
                print(f'F {F:5.2f} nose {tip:4} transverse {transverse:6.3f} : patch semi axes {a:.4f}, {b:.4f} mm; p0 {p/1000:.3f} GPa')
