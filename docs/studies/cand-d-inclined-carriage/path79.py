from finish79 import *
def path():
 r=regions();Hf=capcheck()
 # At own yaw zero, all neighbor outer sectors represented by their own
 # full body shape (including rear of same cover). Split near mating tail.
 B=r['head']+r['shell']+r['front']+r['rear']+r['input']+r['index']+r['coil']+r['body']+r['elec']+[Hf]+r['ram']
 F=r['body']+r['elec']+r['tail']+enclosure()+production()+indexdrive()+blocks()+rearways()+safeties()+fixedguide()+bridge(0)+car(CMAX)+followers(0)+followers(S)+eccentric(0)+eccentric(90)
 # Entire lined cover's remaining material lies outside the front cut
 # (true cylinder r14.10 from x>=-9.68) or behind x=-9.68, or outside outer hull.
 # Test using inscribed polygon window (solid superset of the actual cut-side wall).
 dw,v,vi,vo=covers()
 cap=max(q[0] for q in vo);rad=max(np.linalg.norm(q[1:]) for q in vo)
 wall=ann('conservative cover after front bore',[-9.68,0,0],[cap,0,0],14.10,rad,96)
 # Rear halfspace and exterior cylinder must ALSO be clipped to the cover
 # outer x extent. Bounding box clips only in X for this pessimistic test.
 wall+= [bx('conservative cover rear slab',(min(q[0] for q in vo),-9.68),(-40,40),(-40,40))]
 # Neighbor outside its mating tail. For whole +X then -Y path, its bare
 # remaining body and cover start x>=..., zmin each table foot unaffected.
 for nm,a,b in [('first',[0,0,0],[6.55,0,0]),('second',[6.55,0,0],[6.55,-7,0])]:
  motion=np.array(b)-a
  N=sweep(move(B, PITCH*X+np.array(a)),motion)
  # pass hulls as actual conservative sweeps; nominal zero-yaw, not all poses
  print(nm,'outside body all along, with cover and attached receiver tail',pairs(B+r['tail'],N))
  nt=sweep(move(tail(),np.array(a)),motion)
  print(nm,'mating tail vs 79-only outside stock',pairs(F,nt),'vs cover aperture superset',pairs(wall,nt))
  # Split upper-guide and other head extensions, retaining Take74 nominal
  # caps separately. Test actual newly lowered cages, struts, entire hood.
  ne=[q for q in lip() if not q[0].startswith(('barrel ','rear bore bulkhead'))]
  print(nm,'all changed nose guides and struts',bpair(ne,nt,2))
  wr=[q for q in lip() if q[0].startswith(('barrel ','rear bore bulkhead'))]
  # Concentric nominal tube is faceted; any negative broad result not a collision.
  print(nm,'unchanged shape of tube / bulkhead',bpair(wr,nt,1))
 print('terminal ram/key at PARK, ram vs endpoint lug',pairs(move(keyplus(),S*Y),sweep(ejection()[:1],9.35*X)),pairs(move(ejection()[:1],9.35*X),move(tail(),[6.55,-7,0])))
 print('floor z; both listed lowest feet',min(ext(q,np.eye(3))[0][2] for q in B),min(ext(q,np.eye(3))[0][2] for q in B if q[0].startswith('foot (')))
if __name__=='__main__':path()
