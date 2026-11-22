"""Export grouped collision allocations in world mm plus a section for placement."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('horn-package-take48.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Circle,Patch
def scene():
    return {'joint':joint48(),'own_tail_p37.5':tail48(),'mated_thick_interface':[s for s in tail48(0) if s[0].startswith(('eye','heavy','boss'))],
            'face_home':face3(),'X_mover_home':xmove(),'X_mover_and_face_recovery':fp(face3()+xmove()),'X_fixed':xfixed(),
            'horn_closed':horn(L,0)+fork5(),'horn_parked':horn(L,0,pk)+fork5(pk),'horn_sweep':horn(L,0,0,pk)+fork5(0,pk),
            'hardware_except_cam_web_groove':[s for s in drive() if s[0] not in ('cam solid rear web','grooved cam envelope')],
            'cam_closed_flanks_and_web':camstock(),'cam_parked_flanks_and_web':camstock(pi),
            'cam_full_rotation_bound':[s for s in drive() if s[0] in ('cam solid rear web','grooved cam envelope')],
            'lever_closed':lever(),'lever_parked':lever(pk),'index_dog_blanks_and_sweep':indexdog(),
            'fixed_bearings':che5(),'front_hood':roof48(),'rear_cap_before_duct_ports':hoodoutside()[-1:],
            'rear_duct_outer_envelope':duct(),'electrical_and_feet':packageElec()}
def main():
    S=scene();obj={'units':'mm','L':L,'p':P,'k':0,'format':'[name,convex-hull vertices,offset radius, disk normal or null for isotropic offset]. Allocation model, not boolean manufacturing CAD; see report. Do not union simultaneously exclusive states.',
                   'groups':S}
    Path(__file__).with_name('horn-model-take48.json').write_text(json.dumps(obj,separators=(',',':'))+'\n')
    fig,axs=plt.subplots(1,3,figsize=(14.5,5.15),constrained_layout=True)
    def draw(ax,ss,i,j,col,alpha=.28):
        for _,v,r,a in ss:
            vs=np.array(v);points=[]
            for th in np.linspace(0,2*pi,24,endpoint=False):
                u=np.zeros(3);u[i]=cos(th);u[j]=sin(th)
                if a is not None:u-=np.dot(u,a)*np.array(a)
                ps=vs if not r or np.linalg.norm(u)<1e-12 else vs+r*u/np.linalg.norm(u)
                points.extend(ps[:,[i,j]])
            points=np.array(points)
            if len(points)<3 or np.linalg.matrix_rank(points-points[0])<2:continue
            h=ConvexHull(points);ax.add_patch(Polygon(points[h.vertices],closed=True,fc=col,ec=col,alpha=alpha,lw=.35))
    a,b,c=axs
    draw(a,roof48(),0,2,'#526981');draw(a,tail48(),0,2,'#86979c',.20);draw(a,fork5()+horn(L,0),0,2,'#cb6034',.65)
    draw(a,fork5(pk)+horn(L,0,pk),0,2,'#228a7b',.35);a.scatter(*O,color='#131e2d',s=23);a.text(O[0]-2,O[1]-2.7,'O')
    a.set(xlim=(-32,19),ylim=(-14,28),title='A   |   Horn and rear-open hood',xlabel='X  /  mm',ylabel='Z  /  mm')
    draw(b,camstock(),0,2,'#526981',.30);draw(b,lever(),0,2,'#cb6034',.56)
    for name,ctr,rad in [('C',C48,5.4),('I',IC,5.4),('M',M48,1.8)]:
        b.add_patch(Circle(ctr,rad,fill=False,color='#248375',lw=1.1,linestyle='--'));b.text(ctr[0],ctr[1],name,ha='center',va='center',fontsize=8)
    b.set(xlim=(-17,14),ylim=(-4,25),title='B   |   Closed cam and roller',xlabel='X  /  mm',ylabel='Z  /  mm')
    for s,col in [(packageElec()[:1],'#d29c38'),([s for s in boards() if s[0]=='MCU'],'#625a97'),([s for s in xfixed() if s[0]=='X gearmotor'],'#cb6034'),(camstock(),'#526981')]:
        draw(c,s,0,1,col,.46)
    for name,p,w in certify(actualpoints(0))[1]:c.plot(p[0],p[1],'o',color='#182737',ms=4)
    c.set(xlim=(-25,22),ylim=(-30,30),title='C   |   Four Ø62.588 witnesses',xlabel='X  /  mm',ylabel='Y  /  mm')
    for ax in axs:ax.set_aspect('equal');ax.grid(True,color='#b7c0c6',alpha=.28);ax.set_axisbelow(True)
    a.legend(handles=[Patch(color='#cb6034',label='closed'),Patch(color='#228a7b',label='parked')],loc='lower right',fontsize=8)
    c.legend(handles=[Patch(color=v,label=n) for v,n in [('#d29c38','cell'),('#625a97','MCU'),('#cb6034','X motor'),('#526981','rear web')]],loc='lower left',fontsize=8)
    fig.suptitle('Take 48  /  L18 · p37.5 · k0     |     Placement sections, not clearance proofs',fontsize=15)
    fig.savefig(Path(__file__).with_name('horn-section-take48.png'),dpi=150)
if __name__=='__main__':main()
