"""Tilted 65-degree contact arrangement; signed service loads in HEAD axes."""
from tight import *
BOXES={'service':[2.745862,.686466,.686466,31.5774,34.8724,120.7836],
 'table':[3.432328,.686466,.686466,48.7391,62.3311,167.8285],
 'fault':[2.745862,.686466,.686466,31.5774,34.8724,169.0970]}
def capload(pp,nn,mu,b,N,outer):
    f,w=basis(pp,nn,mu,N,outer); best=-1
    for i in range(1,7):
        ix=np.arange(7)!=i;A=w[ix].reshape(-1,6).T; obj=np.repeat([-1,0,0,0,0,0],N)
        lp=linprog(obj,A_ub=np.vstack([A,-A]),b_ub=np.r_[b,b],bounds=(0,None),method='highs')
        assert lp.success
        if -lp.fun>best:
            best=-lp.fun;act=np.zeros((7,3));act[ix]=(lp.x.reshape(6,N,1)*f[ix]).sum(axis=1)
            out=dict(max_key=best,missing=i,seat_forces=act,external=-(A@lp.x)*[1,1,1,BR,BR,BR])
    return out
def loads():
    out={}
    tight_data=json.loads(Path(__file__).with_name('tight.json').read_text())
    eta=tight_data['all_missing_lower']
    for k,b0 in BOXES.items():
        b=np.array(b0)/[1,1,1,BR,BR,BR]
        ex=capload(PP,NN,.23,b,512,False);hi=capload(PP,NN,.23,b,512,True)['max_key']
        n1=NN.copy()
        for i,f0 in enumerate(ex['seat_forces']):
            tg=f0-(f0@NN[i])*NN[i]
            if norm(tg)>1e-8:
                da=min(radians(.099),atan2(norm(tg),NN[i]@f0))
                n1[i]=cos(da)*NN[i]+sin(da)*tg/norm(tg)
        tol=capload(CC+O-R*n1,n1,.23,b,128,False)
        # Inscribed witness scaled to practical load: actual 20um missing
        # plane. All other planes, rigid tail, and key stay exactly nominal.
        out[k]=dict(head_frame_box=b0,zero_mu=capload(PP,NN,0,b,4,False)['max_key'],
           mu015=capload(PP,NN,.15,b,64,False)['max_key'],
           nominal_dry_bracket=[ex['max_key'],hi],
           actual_witness=ex,example_60N_external=ex['external']*(60/ex['max_key']),
           nominal_dry_110g=[x*(110/70) for x in (ex['max_key'],hi)],
           allowed_tolerance_lower_witness=tol,altered_normals=n1,
           rough_sufficient_under_tolerance=norm(b)/eta,
           already_seated_normal_solution=hold(b))
        assert np.max(np.abs(ex['external'])-b0)<1e-6
    return out
def hold(b):
    # Distinct result: a positive, zero-tangential-force solution exists
    # for every box corner, PROVIDED all seven contacts have been verified.
    # The first scalar interval in tight.py bounds G=0 poses as well.
    th=radians(.367);en=2*sin(ERR/2);ds=hypot(en,th+en)
    dk=hypot(en,(th+en)*2/BR)
    w,N=clean(PP,NN);L=np.linalg.inv(w[:,1:])
    sv=np.linalg.svd(w[:,1:],compute_uv=False)[-1];assert sv>sqrt(6)*ds
    d=cos(radians(65)+ERR);bd=abs(U)@b[:3]
    sz=np.linalg.norm(L,axis=1)
    coeff=N-sz*(dk+ds/d)
    delta=np.abs(L)@b+sz*ds*bd/d
    need=max(delta/coeff)
    assert min(coeff)>0 and need<60
    active=60.;maxseat=(active+bd)/d
    E=210e3/(2*(1-.3**2))
    return dict(actual_key_normal_sufficient=need,
       at_60N_min_seat_solution=min(coeff*active-delta),
       at_60N_sum_seats=maxseat,conditional_hertz_key_radius=(3*active*R/(4*E))**(1/3),
       worst_seat_patch_radius=(3*maxseat*R/(4*E))**(1/3))
if __name__=='__main__':print(json.dumps(loads(),default=serialize,indent=2))
