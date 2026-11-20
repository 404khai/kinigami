"""Screen an instrumented *axial* draw and a permanently engaged alternative.
N, mm, N mm. A motor command is neither an observation nor an upper force cap.
"""
from itertools import product
from math import cos, pi, sqrt

def coeff(radius,lead,mu,up):
    q=lead/(2*pi*radius)
    f=mu/cos(pi/6)
    return radius*((f+q)/(1-f*q) if up else (f-q)/(1+f*q))

def window():
    # From v7, 50 g reference and conservative 50.8 mm pitch.
    W=.050*9.80665
    M=(14.5**2+(50.8*W)**2)**.5
    # Equilateral axial pads; minimum barycentric weight for a bending
    # resultant is (p - 2M/R)/3. This is axial statics only.
    need=4*W+2*M/4.65
    print(f'All-three-contact min axial preload (no parasitic moments) > {need:.3f} N')
    # Smalley CMS08-M1. Assume an INDEPENDENT acceptance band at nominal
    # working height to expose sensitivity. REF rate not a tolerance.
    F0,K=30.,28.85
    forces=[F0*(1+s)+K*(1+u)*h for s,u,h in product((-.12,.12),(-.15,.15),(-.08,.08))]
    print('If load +/-12%, rate +/-15%, actual height +/-0.08:',round(min(forces),2),round(max(forces),2),'N')
    print('Ratios to min axial preload',round(min(forces)/need,2),'and rated-axial-domain screen only')
    # Upper condition measured at actual stroke, not a proposed catalogue guarantee.
    for r,pitch in ((1.25,.35),(1.50,.50)):
        for mu in (.08,.23):
            up,down=[coeff(r,pitch,mu,b) for b in (True,False)]
            q=49.03-8.0 # illustrative NON-thread torque allocation
            print(f'r={r:.2f} lead={pitch:.2f} mu={mu:.2f} raise/lower={up:.3f}/{down:.3f} mm, conditional raise budget={q/up:.1f} N')
    # Symmetric physical torque-limiter sensitivity. With a blocked slider, a
    # multistart screw trades working force for lower reverse breakaway, even
    # if it tightened at zero friction and reverses dry. No self-lock credit.
    lo,hi,other=30.,37.,5.
    for pitch in (.35,.5,1.5,2.0):
        r=1.5
        Fmax=hi/coeff(r,pitch,0,True)
        rev=Fmax*max(0,coeff(r,pitch,.23,False))+other
        work=(lo-other)/coeff(r,pitch,.23,True)
        print(f'lead {pitch:.2f}: within 30..37 Nmm delivered cap, zero-friction jam <= {Fmax:.1f} N; worst reverse with reserved drag {rev:.1f} vs {lo}; dry work budget {work:.1f} N')
    # Drawbolt last thread: generous smooth *cylindrical* full-shear-area
    # ceiling, NOT a screw allowable, tau=1000 MPa is illustrative.
    # Actual helical flank/runout generally has less area.
    f=4*W
    d,tau=3.0,1000.
    for ell in (.1,.01,.001,.0001):
        print(f'ell={ell:.4f} mm nominal generous area*piD: F ceiling {pi*d*ell*tau:.3f} N')
    print(f'At 4W={f:.3f} N, even this assumed strength ceases to support static force below {f/(pi*d*tau):.6f} mm nominal overlap.')
    print('Not proof of physical damage: at the end, real elastic or dynamic separation and rounded load handoff replace this static idealization.')
    # A positive pusher cannot reduce tail tensile demand while a direct mating screw is still its only tensile carrier.
    assert min(forces)>need and max(forces)<40
if __name__=='__main__':
    window()
