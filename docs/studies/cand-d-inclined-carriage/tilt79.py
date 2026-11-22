from path79 import *
def tilt():
 r=regions();F=r['body']+r['elec']+r['tail']+enclosure()+production()+indexdrive()+blocks()+waystock()+safeties()+fixedguide()+sweep(bridge(0),CMAX*Y)+sweep(followers(0),S*Y)+eccentric(0)+eccentric(90)
 delta=10.65*U;N=sweep(tail(),delta)
 ne=[q for q in lip() if not q[0].startswith(('barrel ','rear bore bulkhead'))]
 print('continuous 10.65 mm registered D draw advance XY',delta,'new guide/ties to entire swept tail',bpair(ne,N,1),'rear stock to swept tail',bpair(F,N,1))
 dr=sweep(keyplus()[1:],S*Y)
 # Adaptive axes on the convex difference: any projection gives a true
 # lower bound, even if local optimization misses the exact closest axis.
 vals=[]
 for h in ne:
  for q in N:
   v=pairs([h],[q])[0]
   if v<.50:
    def gap(t):
     ax=np.array([[cos(t[0])*cos(t[1]),sin(t[0])*cos(t[1]),sin(t[1])]])
     return float(ext(q,ax)[0][0]-ext(h,ax)[1][0])
    for t in ((3.1,0),(-1.57,0),(-1.3,0),(0.,0.),(1.57,0.)):
     a=minimize(lambda u:-gap(u),t,method='Nelder-Mead',options={'xatol':1e-8})
     v=max(v,gap(a.x))
   vals.append((v,h[0],q[0]))
 print('support-refined minimum continuous D draw gap',min(vals))
 print('all original key shoe extensions: all stroke vs all draws conservative independent',pairs(dr,N))
 B=r['body']+r['elec']+r['input']+r['head']+r['rear']+[capcheck()]
 print('outer neighbor body vs outer receiver body and yaw shaft through D',pairs(B+r['tail'],sweep(move(B,PITCH*X),delta)))
 print('original key work-point support remains result of inclined 74, not a statement that tail is compelled to draw')
 print('screw wheel, gear radial guide and cell vs upper parked metal',pairs(move(keyplus(),S*Y),production()+[q for q in r['elec'] if q[0]=='cell bulk']))
 # rear cut r<=10.85 x<=-23.60: check one clear ray directed -X from
 # auxiliary motor through actual window, full fixed and contacts without
 # convex-shell false body. Only unintended reach if downstream rays clear.
 q=next(q for q in indexdrive() if q[0]=='remote index 0615 256')
 xx= MOT[0]-sqrt(3**2-(9.72-MOT[1])**2)
 tool=ax('probe R.20',0,-49,xx-.03,(9.72,0),.20)
 groups=regions()
 ex=[p for k,g in groups.items() for p in g if p[0] not in (q[0],'index rotor lower guard')]
 print('rear opening radial margin for inspection probe',10.85-9.72-.20,'ray ends x',xx-.03,'gap other stock',bpair([tool],ex,1))
if __name__=='__main__':tilt()
