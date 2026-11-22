"""Editable grouped Take 50 layout in world mm. No manufactured B-rep."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('horn-socket-take50.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def groups():
    return dict(joint_v3=joint51(),own_tail_v3=tail51(),mated_stock=[s for s in tail51(0) if s[0].startswith(('eye','boss','heavy'))],
                idle_bearings_and_frame=cheeks50(),root_drive=drive50()+guides(),closed_hold=keyparts(0),lifted_hold=keyparts(4.70),
                dog_hardware_and_sweep=grip50(),horn_closed=rotor(0),horn_parked=rotor(PH),horn_sweep=rotor(0,PH),
                root_closed=rodparts(0),root_parked=rodparts(PH),root_sweep=stages(),face_home=F51,
                face_drive_fixed=lowfixed(),face_carriage_home=lowmoving(),face_and_carriage_range=fp(face50()),
                forward_hood=roof51(),aft_blank_not_a_closure=hood51()[-1:],outer_rear_garage_allocation=shell50(),
                socket_replacement_not_additive=socket(),separator_T49_home=tiles('home'),
                overload_sense_flags=extra(),electrical_and_feet=parts()+feet)
def export():
    gr=groups(); path=Path(__file__).parent
    doc={'label':'exploratory','units':'mm','inputs':'Take51 interface v3; Take49 low-cap-v3 home; exact seven phases/interpolation supplied in take49-low-cap-v3-sweep.json','datum':{'pitch':P,'H':H,'O':O48,'k':0,'phi_open':PH},
         'shape':['name','convex-hull vertices','offset radius','disk-normal axis (null = isotropic offset)'],
         'note':'Closed/parked/range are separate states, not superposed material. Some circles represent allocated gear blanks or assembled outer dimensions, not teeth/bores. Socket group is a separate alternative replacing central gauged neck/backing; not additive. Garage is outer reserved volume of a merged chamber, not filled stock; aft panel blank is not a closure.',
         'groups':gr}
    (path/'horn-model-take50.json').write_text(json.dumps(doc,separators=(',',':'))+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    fig,ax=plt.subplots(1,2,figsize=(13,6),layout='constrained')
    for a,(j,h) in zip(ax,[(0,2),(1,2)]):
        def paint(S,color,alpha):
            for s in S:
                _,v,r,d=s;p=np.asarray(v)[:,[j,h]]
                if r>0:
                    direction=np.c_[np.cos(np.arange(32)*pi/16),np.sin(np.arange(32)*pi/16)]
                    if d is not None:
                        da=np.array(d)[[j,h]];ev,rot=np.linalg.eigh(np.eye(2)-np.outer(da,da))
                        direction=direction@rot@np.diag(np.sqrt(np.maximum(0.,ev)))@rot.T
                    p=(p[:,None,:]+r*direction[None,:,:]).reshape(-1,2)
                if len(p)<3 or np.linalg.matrix_rank(p-p[0])<2:continue
                a.add_patch(Polygon(p[ConvexHull(p).vertices],closed=True,color=color,alpha=alpha,lw=.5))
        paint(gr['own_tail_v3'],'#ad8a67',.10);paint(gr['joint_v3'],'#627182',.19);paint(gr['face_home'],'#326598',.23)
        paint(gr['face_drive_fixed']+gr['face_carriage_home'],'#275799',.50);paint(gr['idle_bearings_and_frame'],'#655581',.28)
        paint(gr['horn_closed']+gr['root_closed'],'#ab6228',.55);paint(gr['horn_parked']+gr['root_parked'],'#33918b',.22)
        paint(gr['root_drive']+gr['closed_hold'],'#19715c',.44)
        a.set(xlim=(-37,30),ylim=(-27,30),aspect='equal',xlabel=('X' if j==0 else 'Y')+' (mm)',ylabel='Z (mm)')
        a.axhline(-23.65,color='#666',lw=.9,ls='--');a.grid(alpha=.15)
    fig.suptitle('Take 50  |  buried-root slider and low fixed rails',fontsize=17)
    fig.supxlabel('Brown: closed horn/link   ·   Teal: parked   ·   Green: root drive   ·   Blue: moving face / X drive\nProjections for navigation only; electronics, garage, terminal and tolerance not shown.',fontsize=10)
    fig.savefig(path/'horn-section-take50.png',dpi=128);plt.close(fig)
    print('export',len(gr),'groups',sum(map(len,gr.values())),'convex components')
if __name__=='__main__':export()
