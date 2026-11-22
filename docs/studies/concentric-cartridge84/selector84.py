from survey84 import *
def main():
 b=book();rows=[]
 for angle in np.linspace(-73,73,147):
  # Registered nut/draw holes at both travel endpoints; their material is then stationary
  # while the sequencer moves. No fictitious simultaneous main drive motion.
  for ph,t in [('LOCK',0),('DRAW',1),('PARK',0)]:
   m=pose(b,ph,t,0,selector=angle);gg={}
   for g,cam,pin,disc in [('spin','sleeve closed cam','sleeve index pin','rotating hollow nut'),('dpin','draw closed cam','draw index pin','draw index disc')]:
    ff=m[g+' follower'];q=m[cam];pp=m[pin];discq=m[disc];aa=m[g+' return fork']
    pairs=[(q,ff),(pp,discq),(q,m[g+' slider shoe']),(aa,m['selector 0615/06-1'])]
    gg[g]=[round(max(0.,(x^z).volume()),7) if cand(bb(x),bb(z)) else 0 for x,z in pairs]
   rows.append([angle,ph,t,gg])
 dump('selector84.json',dict(label='exploratory',columns=['cam/follower','dog/indexed flange','cam/slider','return fork/selector housing'],rows=rows,note='Imposed selector stroke about fixed registered axes, both endpoint configurations. No proof of positive motor key engagement, lateral yoke guidance, shaft realignment, load transfer, or actuation under power loss mid-stroke.'))
if __name__=='__main__':main()
