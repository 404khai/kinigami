"""A posteriori separator bounds for the tighter tilted 65-degree study."""
from compare import *
from scipy.spatial.transform import Rotation
O=np.array([BC,0.,0.]);PP,NN,CC=tilted();CC-=O
U=-NN[0]; ERR=radians(.10);NLINE=48
FF=np.array([rays(nn,.23,NLINE,True) for nn in NN]); SS=np.cross(NN[:,None,:],FF)
FC=np.array([rays(nn,tan(atan(.23)+ERR),NLINE,True) for nn in NN])
def certify(k,origin,half,tw=None,J=None):
    # Actual sphere centers translated collectively (sum F=0) and rotated
    # with a COMMON omega from exp coordinates; linearize at identity,
    # debit exact quadratic remainder, independently at every pole.
    cp=Rotation.from_rotvec(origin).apply(CC)
    W=np.concatenate([FC,np.cross(cp[:,None,:]-R*NN[:,None,:],FC)/BR],axis=-1)
    use=~np.isin(np.arange(7),k)
    if tw is None:
        A=W[use].reshape(-1,6)
        lp=linprog([0]*6+[-1],A_ub=np.column_stack([-A,np.ones(len(A))]),
              b_ub=np.zeros(len(A)),bounds=[(-1,1)]*6+[(None,None)],method='highs')
        tw=lp.x[:6]
    v,w=tw[:3],tw[3:]
    t=v+np.cross(w,cp)/BR
    raw=(FF*t[:,None,:]).sum(axis=-1)-R/BR*(SS*w).sum(axis=-1)
    # An actual normal within ERR is precisely a minimal rotation of its
    # nominal Coulomb cone; rotate force AND the ball-offset friction spin.
    grad=np.cross(FF,t[:,None,:])-R/BR*np.cross(SS,w)
    grad-=NN[:,None,:]*(grad*NN[:,None,:]).sum(axis=-1)[:,:,None]
    kappa=hypot(1,.23/cos(pi/NLINE))
    err_n=ERR*np.linalg.norm(grad,axis=-1)+.5*ERR**2*kappa*(
        np.linalg.norm(t,axis=-1)[:,None]+R/BR*norm(w))
    grad_pose=np.cross(CC[:,None,:],np.cross(FF,w))/BR
    reach=np.linalg.norm(CC,axis=-1)[:,None]/BR
    # Optionally choose an affine, configuration-dependent separator across
    # the whole cell. J need not be the derivative of an optimal solution.
    add=0.;yn=norm(tw)
    if J is not None:
        exact=np.concatenate([FF,(np.cross(cp[:,None,:],FF)-R*SS)/BR],axis=-1)
        grad_pose+=exact@J
        jy,jw=norm(np.abs(J[:3])@half),norm(np.abs(J[3:])@half)
        # Cross-products of changing twist with uncertain cone or center.
        add=kappa*(ERR*(jy+jw*(reach+R/BR))+norm(half)*reach*jw)
        yn+=hypot(jy,jw)
    err_pose=add+np.sum(np.abs(grad_pose)*half,axis=-1)+reach*kappa*norm(w)*(
             (norm(origin)+.5*norm(half)+ERR)*norm(half))
    value=(raw-err_n-err_pose)[use].min()
    return (value-1e-10)/yn,tw
def field(origin,k=1):
    z=np.zeros(3);t=certify(k,origin,z)[1]
    J=np.column_stack([(certify(k,origin+d*1e-5,z)[1]-certify(k,origin-d*1e-5,z)[1])/2e-5 for d in np.eye(3)])
    return t,J
def cover(k,line,Rtube,root,threshold,min_half=radians(.002)):
    # Cells outside the capsule about a segment cannot contain a valid
    # orientation. C3 symmetry + reflection sends every single missing face
    # to pole 1; norm/angular balls are invariant under those transformations.
    lo,hi=line;delta=hi-lo;l=norm(delta)
    oref=(lo+hi)/2;t,J=field(oref,k)
    seen=0;worst=1.;stack=[root];eps=1e-12
    while stack:
        o,h=stack.pop()
        par=np.clip((o-lo)@delta/(l*l),0,1) if l else 0.
        if norm(o-lo-par*delta)>Rtube+norm(h)+eps:continue
        x,_=certify(k,o,h,t+J@(o-oref),J);seen+=1
        if x<=threshold and isinstance(k,list):
            x=certify(k,o,h)[0]
        if x>threshold:worst=min(x,worst);continue
        if max(h)<min_half:
            raise ValueError(('uncertified',k,np.rad2deg(o),x,seen))
        j=int(np.argmax(h));g=h.copy();g[j]/=2;d=np.eye(3)[j]*g[j]
        stack.extend([(o-d,g),(o+d,g)])
    return seen,worst
def tight():
    D=np.linalg.inv(clean(PP,NN)[0][:,1:].T)
    verts=np.array(list(product([-1,1],repeat=6)))@D.T
    Kt=max(norm(r[:3]) for r in verts); Kr=max(norm(r[3:]) for r in verts)
    theta0=radians(5);t0=1.
    en=2*sin(ERR/2);d0=.020+R*en**2/2
    cap=.020+(-2.68+2.12)+R*(cos(radians(65))+en)
    maxgap=2*cos(radians(65))*cap+2*en*(t0+theta0*BR)+2*d0
    assert maxgap<.50
    one=[];z=np.zeros(3)
    for a1,a2 in zip(np.arange(10)*.05,np.arange(1,11)*.05):
        # An occupied primary plane fixes the nominal ball-center residual;
        # for the missing one add G, not just its manufacture recess.
        th,tx=theta0,t0
        for _ in range(12):
            e=d0+en*(tx+BR*th)+.5*BR*th**2
            th=min(th,(norm(D[3:,0])*a2+Kr*e)/BR)
            tx=min(tx,norm(D[:3,0])*a2+Kt*e)
        Rtube=Kr*e/BR+1e-11;lo=D[3:,0]*a1/BR;hi=D[3:,0]*a2/BR
        o=(lo+hi)/2;h=np.abs(lo-hi)/2+Rtube
        c,m=cover(1,(lo,hi),Rtube,(o,h),.00005)
        one.append(dict(gap_interval=[a1,a2],radius_deg=degrees(Rtube),boxes=c,lower=m))
    two=[]
    # With two V faces absent, test every remaining face pair excluding 1
    # and j. The positions not constrained by the missing planes can vary
    # freely in the whole stated 5-degree rotation ball.
    for j in range(2,7):
        c,m=cover([1,j],(z,z),theta0,(z,np.full(3,theta0)),.00005)
        two.append(dict(second_missing=j,boxes=c,lower=m))
    return dict(actual_pole_error=degrees(ERR),head_frame_recess=.020,
       pose_limit_deg=degrees(theta0),trans_limit_mm=t0,single_gap_cap=maxgap,
       five_seat_results=one,fewer_seat_results=two,
       all_missing_lower=min(x['lower'] for x in one+two))
if __name__=='__main__':
    print(json.dumps(tight(),default=serialize,indent=2))
