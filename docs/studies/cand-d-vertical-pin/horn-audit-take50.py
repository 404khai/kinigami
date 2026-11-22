"""Selected physical witnesses and sensitivity. Does not infer ratings or co-motion."""
from runpy import run_path
from pathlib import Path
G=run_path(str(Path(__file__).with_name('horn-package-take50.py')))
globals().update({k:v for k,v in G.items() if not k.startswith('__')})
def audit():
    print('version H',H,'pitch',P,'rail shoe span',XR1-XR0)
    for n,A in [('bearing+mount',cheeks50()),('idle rotor',rotor(0,PH)),('upper drives+extra',allmotor()+extra()[:1]),
                ('upper links',stages()),('lower+moving',lowfixed()+fp(lowmoving()))]:
        print(n,'own tail+allowance',ytest(A,tail51(),1)[:2],flush=True)
    boss=[sh('outer bound'+str(sg),*sorted([sg*9.39,sg*12.50]),O,4.10) for sg in (-1,1)]
    print('short cartridge bound / tail',ytest(boss,tail51(),1)[:1],'yaw can',fastpair(boss,[v for v in joint51() if v[0]=='yaw gearmotor'])[:1])
    for n,b in [('body',joint51()),('own tail',tail51())]:
        print('U skirt/backing thru X versus '+n, (fastpair(fp(lowmoving()),b) if n=='body' else ytest(fp(lowmoving()),b,1))[:3])
    print('cartridge support/pinned link',fastpair(cheeks50(),stages(num=20))[:3])
    print('v3 gear and supporting return, nominal',fastpair([s for s in cheeks50() if s[0]=='v3 cheek mounting return'],joint51())[:4])
    print('point comparison centre rib vs hub +X relief v3',lp(F51[-1],next(s for s in tail51() if s[0]=='tail sector hub0')))
    # Fixed motor in next Kin vs actual external moving keel. A box-centre line
    # with z above motor centre is enough; no SAT negative or imposed co-motion.
    m=next(s for s in lowfixed() if s[0]=='face Y motor')
    x,y,z=m[1][0];rr=m[2];zb=-18.32;yb=4.72;xm=x+P
    xx=next(s for s in lowmoving() if s[0]=='moving keel 1')
    gap=xm-sqrt(rr*rr-(zb-z)**2)-proj(xx,X)[1]
    print('aligned rail static gap',P+proj(lowfixed()[0],X)[0]-proj(lowfixed()[0],X)[1])
    print('held neighbour keel line onset by stroke',gap,'full endpoint common point',(xm,yb,zb),'motor bore depth to OD',rr-abs(zb-z),'keel box',ab(mx(xx,END)))
    print('6-phase bar legacy example and foot / Y motor (NOT INCLUDED in geometry):',hypot(*sub((1.25,16.,32.812),(-13.3,-9.75,-23.50))),hypot(1.25-x,32.812-z)+rr, 'motor 3D far distance',far(m,(1.25,16,32.812)))
    # Supported iff exterior rate/lash calibration and strength established.
    jmin=15.86304;hmin=15.68436
    for T in (246.,1742.,1742*200/163):
        F=T/jmin;Q=T/hmin;V=.389*F;S=7.8
        N=V+2*(F*abs(ZH-ZS)+V*1.5)/S
        for mu in (.10,.23):
            ecc=abs(ZH+.72-ZS)+4.35
            dr=mu*N/(1-2*mu*ecc/S);thr=F+dr;ratio=22/34*38/34
            print('root T mu, ideal axial, link, transverse, guide friction, thrust, required gearhead @ .28/.75',T,mu,F,Q,V,dr,thr,thr*.50/(2*pi*.28*ratio*.75))
        print('opening lash arc @r18 (2x radial .025 and .08 dog gap), pin shank Euler etc separate',18*(.05/hmin+.08/jmin),'link elastic shortening and arc',Q*8/(200e3*2.10*2.8),18*Q*8/(200e3*2.10*2.8)/hmin)
        print('dog key face bearing and nominal bracket moment, centre-line link contribution per short radial bearing upper bound',F/(4*(3.15-1.98)),F*8,Q*12.5/(12.5+9.39))
    print('radial external force term per end <= coefficient, side-force overturning term at R<=23.2, max nominal stub bent at y7.25 MPa/N', (12.5+4.27)/(12.5+9.39),23.2/(2*9.39),32*(12.5-7.25)/(pi*4**3))
    print('thrust face gross annulus area mm2, projected radial area',pi*(2.86**2-2.06**2),4*2.98)
    for f in (111.,155.,163.,200.):
        print('centred axial-only trial / broad gauged web MPa',f,f*17.3/(14.4*2.36**2/6))
    print('signed contact whole horn vs independent rod central stock: tangent plane s<=0, rod root eye minimum',SS-2.35,'spoke maximum',1.65)
    # Real power-off domain is the closed hold only: key disengaged during motion.
    # Full key sweep intersects moving block intentionally; retracted lower face:
    print('retracted required lift to clear moving block with 0.15',3.15+.15-1.,'locating shaft end play',9.39-9.34,12.56-12.50)
    y=NC-5.50-.08-.80;lo=NC-7.24;stem=y-.75
    print('closed dog register gap, back guide stem clearance and max rigid one-sided pole arc including pin radial play',.08,stem-lo,18*(.05/hmin+(.08+stem-lo)/jmin))
    block=next(s for s in rodparts(0) if s[0]=='dog register block')
    key=keyparts(4.7)[0];print('released key lower to closed block upper',proj(key,Z)[0]-proj(block,Z)[1])
    print('floor lower stock',min((proj(s,Z)[0],s[0]) for s in fixed50()+face50()+parts()+slide50(0)+feet+tail51()))
if __name__=='__main__':audit()
