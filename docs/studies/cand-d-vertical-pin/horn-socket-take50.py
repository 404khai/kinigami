"""Separate paired-web variant. Loads/signed witnesses, not a rated interface."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('horn-tiles-take50.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def socket():
    v=[]
    for sg in (-1,1):
        def yy(l,h):return tuple(sorted((sg*l,sg*h)))
        # One long planar rib at each side; rear and forward attachment toes
        # face away from one another. Existing working lands left in place.
        yz=yy(14.8,16.65)
        for n,profile in [('aft',[(2.55,-17.75),(4.86,-17.75),(4.86,12.14),(2.64,12.14),(2.55,-6.85)]),
                          ('fore',[(5.38,-17.75),(9.95,-17.75),(9.95,-12.30),(6.04,12.14),(5.38,12.14)])]:
            v.append(poly('side socket '+n+str(sg),[(x,y,z) for x,z in profile for y in yz]))
        v.append(box('rib base saddle'+str(sg),(-.2,10.60),yy(13.55,17.64),(-18.73,-16.94)))
        # Cross-sill sweeps with the carriage, seats directly on the keel.
        v.append(box('rib cross sill'+str(sg),(-.2,10.60),yy(4.22,16.75),(-18.73,-17.77)))
        for x in (3.55,9.25):
            v.append(box('M2 toe nut boss'+str((sg,x)),(x-1.76,x+1.76),yy(13.80,17.62),(-16.96,-14.78)))
            v.extend([cyl('M2 socket bolt'+str((sg,x)),Z,(-18.76,-15.00),(x,sg*15.71),1.),
                      cyl('M2 head reserve'+str((sg,x)),Z,(-20.02,-18.74),(x,sg*15.71),1.79)])
        for f,zz in [('upper',(9.56,12.65)),('middle',(4.45,6.25))]:
            v.append(box('land transverse backer '+f+str(sg),(2.78,4.93),yy(8.75,16.66),zz))
        for z in (1.4,9.4):
            v.append(cyl('side dowel'+str((sg,z)),X,(3.0,6.00),(sg*15.71,z),.72))
    return v
def examine():
    s=socket();case=lambda A,B:fastpair(A,B)[0]
    print('alternative leaves U-face, replaces central neck/backing with lateral keels/sockets; load pickup at nut thrust before shoe friction')
    print('travel joint, fixed X hardware, own tail, root drive, full rotor, forward hood',case(fp(s),joint51()),case(fp(s),lowfixed()),ytest(fp(s),tail51(),1)[:1],case(fp(s),allmotor()),case(fp(s),rotor(0,PH)+stages()),case(fp(s),roof51()))
    print('mated at aligned home',case(s,[t for t in tail51(0) if t[0].startswith(('eye','heavy','boss'))]))
    for a,b,n in cap49['phases']:
        print('cap relative',n,case(s,ts(a,b,True)))
    for s0 in s:
        for t in tiles('home')+lowfixed()+joint51()+[t for t in tail51(0) if t[0].startswith(('heavy','boss'))]:
            if any(sep(s0,t,d)>0 for d in (X,Y,Z)) or t[2]>0 and t[3] is None:continue
            w=interior(s0,t)
            if w[3]>.005:print('home socket collision',s0[0],t[0],w)
    # At y=8 (right) or -8 (left), in the standalone socket load path,
    # the only cross-section is the 10.8x.96 strip across x,z. A side
    # moment M_y twists it about y. Thin rectangle Saint-Venant estimate.
    for f in (111,170.43,208.30):
        # Rectangular v3 side at z=-7.884. Integral trapezoidal section
        # varies in y from width 9.048 to 8.642 over x=.7. Use true centroid/I.
        b=17.296396143-8.248447295;t=.70;k=(b-8.641948848)/t
        A=b*t-k*t*t/2;xc=(b*t*t/2-k*t**3/3)/A
        I=b*t**3/3-k*t**4/4-A*xc**2;S=I/max(xc,t-xc)
        rise=12.31055+7.88424;h=12.31055+17.80;M=f*h
        print('Fx, U tower single side high-contact illustrative height/Z/stress, old central web centred moment stress',f,rise,S,f*rise/S,6*f*17.30/(14.4*2.36**2))
        print('socket M Nmm; opposing sole force @5.70; one M2 tension MPa @2.07; bushing projected MPa at t1.85*d1.44 (conditional full Fx), tip Z at y14.8..16.65 & effective whole x2.64..6.04, solid upper bound',M,M/5.70,M/(5.70*2.07),f/(1.85*1.44),1.85*(6.04-2.64)**2/6)
        coef=(1/3)*(1-.63*.96/10.80)
        print('if single .96 sill carries entire moment: St Venant shear MPa (no warping restraint), angle rad over 7.5 mm assuming G79GPa',M/(coef*10.8*.96**2),M*7.5/(79000*coef*10.8*.96**3))
        for mu in (.10,.23):
            e=abs(ZSX+18.95)+YRAIL+.98;d=XR1-XR0
            for arm in (abs(ZSX),abs(ZSX)+12.31055):
                T=f+2*mu*f*arm/(d-2*mu*e);print('centred vs high land, mu, ideal one guide couple, thrust, gearhead',arm,mu,f*arm/d,T,T*.5/(2*pi*.28*28/22*.72))
    Path(__file__).with_name('horn-socket-take50.json').write_text(json.dumps(s,separators=(',',':'))+'\n')
if __name__=='__main__':examine()
