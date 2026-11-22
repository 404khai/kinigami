"""Separate contact allocations; never substitute these poles in stock.py."""
from study import *
def critical(p,n,poles=range(1,7),N=32):
    def search(outer):
        lo,hi=0.,.35
        for _ in range(16):
            mid=(hi+lo)/2
            if min(opt(p,n,mid,i,N,outer)[0] for i in poles)>1e-8:lo=mid
            else:hi=mid
        return lo if outer else hi
    return [search(True),search(False)]
def tilted(vdeg=65.):
    # Triad plane normal parallel to actual retaining pull, not global X.
    U=np.array([c,s,0.]);T=u;Z=np.array([0.,0.,1.]);O=np.array([BC,0.,0.])
    C=[O-2*U]; n=[-U];v=radians(vdeg)
    for k in (pi/3,pi,5*pi/3):
        b=O+BR*(cos(k)*T+sin(k)*Z);h=-sin(k)*T+cos(k)*Z
        for sg in (-1,1):C.append(b);n.append(cos(v)*U+sg*sin(v)*h)
    C=np.array(C);n=np.array(n);return C-R*n,n,C
def allocations():
    out=[]
    for vdeg in [45,50,56,60,64,65,70]:
        pp,nn,cc=model(phase=PH,ecc=ECC,v=radians(vdeg))
        fx=min(nn[1:,0]);h=R+.18-R*fx
        out.append(dict(angle=vdeg,mu_loss=critical(pp,nn,range(1,5),24),
               chosen_cap_height_remaining=1.68-h))
    pp,nn,cc=tilted()
    nominal=critical(pp,nn,[1],64) # C3 and mirror symmetry in tilted plane
    # Seek a finite false mount within individual angle tolerances. Build
    # it from a feasible nominal equilibrium just above critical friction.
    val,_,F,_=opt(pp,nn,.239,1,64,False);assert val<1e-9
    n2=nn.copy()
    for i in [0,2,3,4,5,6]:
        t=F[i]-nn[i]*(nn[i]@F[i])
        if norm(t)>1e-8:
            d=min(radians(.59),atan2(norm(t),nn[i]@F[i]))
            n2[i]=cos(d)*nn[i]+sin(d)*t/norm(t)
    pp2=cc-R*n2
    val,_,F2,_=opt(pp2,n2,.23,1,64,False)
    Ns=(F2*n2).sum(axis=1);res=sum(wrench(x,f) for x,f in zip(pp2,F2))
    assert val<1e-9 and norm(res)<1e-9
    # Actual tilted finite V faces in triad coordinates; local cap 2.12,
    # not inherited from the horizontal candidate. Finite facet reserve.
    v=radians(65);t=R*sin(v);h=R+.18-R*cos(v);draft=tan(v)
    flat=min(2.12-h,((3.81-t)*draft-h)/hypot(1,draft),
             (1.35*draft-h)/hypot(1,draft),
             ((12.20-hypot(BR,t))*tan(radians(64))-h)*cos(radians(64)))
    assert flat>.40
    return dict(horizontal=out,tilted=dict(angle=65.,normal_rank=int(np.linalg.matrix_rank(clean(pp,nn)[0])),
       key_lug=cc[0],seat_centers=cc[1::2],nominal_first_loss_mu=nominal,
       nominal_min_at_mu023=min(opt(pp,nn,.23,i,64,True)[0] for i in range(1,7)),
       flat_margin=flat,tower_foremost_bound=BC+c*(-2.68+2.12)+s*11.65,
       bad_pole_normals=n2,bad_contact_positions=pp2,bad_contact_forces=F2,
       actual_projections=Ns,max_friction_ratio=max(norm(f-N*nnn)/N for f,N,nnn in
          zip(F2,Ns,n2) if N>1e-6),max_normal_error_deg=.59,
       missing_pole=1,residual=norm(res)))
if __name__=='__main__':print(json.dumps(allocations(),default=serialize,indent=2))
