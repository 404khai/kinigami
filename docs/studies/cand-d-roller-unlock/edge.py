"""Convex R.25 sleeve toe in contact with a finite R1.50 cylinder."""
from roller import *
E=210000/(2*(1-.3**2)); r=1.5; re=1/(1/r+1/.25); a=radians(8)
R=local(Z,False,False,a,1,False)
def hertz(N,L,r):
    return dict(peak_MPa=sqrt(N*E/(pi*L*r)),halfwidth=sqrt(4*N*r/(pi*L*E)))
if __name__=='__main__':
    nt=45 # illustrative actual normal on ONE tail land; not the force limiter
    ns=nt*R['normal']['sleeve']
    print(json.dumps(dict(label='exploratory',axis=[0,0,1],local_per_tail_normal=R,tail_normal_N=nt,sleeve_normal_N=ns,
       contact_entry_u=-3.80+.25*sin(a),roller_center_u=-3.80+1.75*sin(a),roller_outward=1.75*(1-cos(a)),
       blend_R_eff=re,local_flat=hertz(ns,3,r),convex_blend=hertz(ns,3,re),quarter_length_sensitivity=hertz(ns,.75,re),
       tilt_end_gap_at_halfdeg=3*sin(radians(.5)),blend_Hertz_indentation_scale=hertz(ns,3,re)['halfwidth']**2/(2*re)),indent=2,sort_keys=True))
