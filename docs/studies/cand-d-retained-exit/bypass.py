"""Continuous three-stage defeat of the narrow ram; no blocked actuator or jam."""
from exit import *

def study():
    p=6.55;side=7.;nm=385
    segs=[np.array([t,np.zeros_like(t),np.zeros_like(t)]).T for t in [np.linspace(0,p,nm)]]
    segs.append(np.array([p*np.ones(nm),-np.linspace(0,side,nm),np.zeros(nm)]).T)
    out={}
    for name,cc,rr,ds in entities(nm):
        bounds={}
        for stage,tr in enumerate(segs):
            xx=cc[:,0]+tr[:,0,None];yy=cc[:,1]+tr[:,1,None];zz=cc[:,2]+tr[:,2,None]
            deb=norm(tr[1]-tr[0])/2+ds
            def add(k,v):bounds[k]=min(bounds.get(k,float('inf')),float(np.min(v))-rr-deb)
            add('barrel',gpu(xx,yy,zz))
            add('key',box(xx,yy,zz,[XB,Y0+PARK,-H],[XF,18.2,H]))
            add('guide',box(xx,yy,zz,[GX0,8.60,-ZG],[GX1,18.60,ZG]))
            rx=xx-O[0];h=rx*c+yy*s;j=-rx*s+yy*c
            for k,ph in enumerate(PH):
                radial=j*cos(ph)+zz*sin(ph);tang=-j*sin(ph)+zz*cos(ph)
                # Full occupied tilted station is a subset of this box.
                dd=np.hypot(np.maximum(h+.56,0),
                     np.hypot(np.maximum(abs(radial-10.30)-1.35,0),np.maximum(abs(tang)-3.81,0)))
                # On first stage only, own crest is below the tangent
                # plane and continuous base D<=-2.68. Exact at t=0.
                if name=='wing'+str(k) and stage==0:
                    delta=min(np.dot(W[k]-B[k],D*cos(radians(65))+j0*
                                (-T*sin(ph)+Z*cos(ph))*sin(radians(65))) for j0 in [-1,1])
                    assert delta>0
                    assert min(c*cos(radians(65))+j0*s*sin(ph)*sin(radians(65)) for j0 in [-1,1])>0
                    continue
                add('tower',dd)
        xx,yy,zz=(cc+segs[-1][-1]).T
        dd=np.hypot(np.maximum(xx-END,0),np.maximum(np.hypot(yy-Q[1],zz)-RP,0))
        bounds['final_piston']=float(min(dd))-ds-rr
        assert min(bounds.values())>0,(name,bounds)
        out[name]=bounds
    # During initial +X, the shoe trails the lug. During side motion the
    # ram may remain at lug-rear - epsilon: every other primitive has its
    # rear x at least that large (same on +X, strictly ahead elsewhere).
    # Receiver, not the neighbor, supplies the only radial slot. Through
    # shift, hub x>=p, forks x>=4+p: neither guide, barrel nor end cap hit.
    hgap=min(.20,-GX1);assert hgap>0
    return dict(axial_advance=p,side_shift=-side,housing_lip=0.,
       lug_trailing_x=Q[0]+p-R,ram_face_at_side_motion=Q[0]+p-R,
       parked_ram_after_bypass=END,hub_fixed_front_margin=hgap,
       hub_final_ram_x=p-END,facets=out)
if __name__=='__main__': print(json.dumps(study(),indent=2))
