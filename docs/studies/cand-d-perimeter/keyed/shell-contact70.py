from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-cam70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 cs=core();f=chassis()+pads();si=subset(f,('draw limit','park limit','ring phase','sensor frame','worm','coil','bolt','clamp','yaw motor','yaw main','shaft aft','shaft front','leaf mount','foot','stationary case'))
 print('finished cam core vs unrelated fixed stock',cp(cs,si,6))
 for a in (0,45,85,105):
  z=[lug(a)];print('lug vs all fixed thru hard stops',a,cp(z,f,5),'direct anchored lug/core penetration',cp(z,cs,1))
 for th in (0,20,42,75,105):
  an,dh=phase(th);q=sum((sliders(a,an) for a in AZ),[])
  print('drive links vs flared wall and stop support at',th,cp(q,subset(f,('stationary case','way anchor','park stop outer','leaf mount','leaf bearing','fixed wall heel','outer axial','foot tie','worm fore','thin liner')),5))
 for a in (-15,0,15):
  t=yaw(move(tail(),-P)+joint()[1],a);w=subset(f,('yaw motor','shaft aft','knuckle tang','aft cantilever','outer axial','foot','worm','fixed center quill','draw','park limit','sensor frame','lower yaw','upper yaw','coil','clamp','motor rear'));print('own tail (uncut lobe outer) vs frame/yaw motor',a,cp(t,w,4))
 a=AZ[0];an=0.;l=leaf(a,an)+sliders(a,an);b=cp(subset(l,('external park','bearing pin')),subset(f,('leaf mount','park stop outer','leaf bearing cap','bearing aft tie','thin liner')),5);print('park stub / lever vs outer supports (intended shaft bearings excluded)',b)
 # Exact disk home clearance to fixed bore at home and heel, and
 # stationary axle/lug clearance in radial/axial cut coordinates.
 print('disk rim home/bore gap',bore(HOME)-RD,'plate rear/bore',bore(HOME-1.6)-(RD-.53))
 # Bolt plate vs coil, bush & shaft in both positions. Housing grouping
 # not used for holes. Plate web survives radially and circumferentially.
 dp=next(q for q in f if q[0]=='12 hole parking wheel blank');print('parking plate vs motor and structure',cp([dp],subset(f,('clamp motor','coil shell','worm outboard','coil bracket','motor rear','retract coil','bolt bush')),4))
 print('opposed fixed thrust bearing face to rotating collar nominal gap .015 per side; collar R1.62 on R.93 shaft, fixed plain thrust washer ID.96/OD2.08. 500 and 1500 Nmm nominal average annular thrust pressure MPa',np.array([500.,1500.])/19.5/(pi*(1.62**2-.96**2)))
 # Provide finite clearance sensitivity (not a known system upper). Gear
 # mesh full span=.05 mm at wheel pitch, bolt radial location ±hole and
 # support radial freedom. Worm axial drift adds DIRECT wheel rotation.
 print('illustrative 1-side ring free angle deg for .025 wheel flank, .02 worm axial, .032 dog radial',degrees((.025+.020)/19.5+2*asin(.032/2.62)/130))
if __name__=='__main__':run()
