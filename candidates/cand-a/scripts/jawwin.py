import math
R=25.5; AP=22.0836; V=(-R/2,AP)
def Rot(t,v):
    c,s=math.cos(math.radians(t)),math.sin(math.radians(t)); return (v[0]*c+v[1]*s,-v[0]*s+v[1]*c)
def hex_at(phi,dz=0.0,rc=4.0/math.sqrt(3)):
    q=Rot(-60,(0,0)); c=Rot(phi,(R,0)); c=(V[0]+c[0],V[1]+c[1])
    pts=[]
    for k in range(6):
        u=(rc*math.cos(math.radians(60*k)),rc*math.sin(math.radians(60*k)))
        r=Rot(phi-60,u); pts.append((c[0]+r[0],c[1]+r[1]+dz))
    return pts
def segd(p,a,b):
    ax,az=a;bx,bz=b;dx,dz=bx-ax,bz-az;L=dx*dx+dz*dz
    t=0 if L==0 else max(0,min(1,((p[0]-ax)*dx+(p[1]-az)*dz)/L))
    return math.hypot(p[0]-ax-t*dx,p[1]-az-t*dz)
def inside(p,poly):
    s=None
    for i in range(len(poly)):
        a,b=poly[i],poly[(i+1)%len(poly)]
        cr=(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        if abs(cr)<1e-12: continue
        if s is None: s=cr>0
        elif s!=(cr>0): return False
    return True
def dist_poly_rect(poly,x0,x1,z0,z1):
    rect=[(x0,z0),(x1,z0),(x1,z1),(x0,z1)]
    if any(inside(p,rect) for p in poly) or any(inside(p,poly) for p in rect): return 0.0
    d=1e9
    for P,Q in((poly,rect),(rect,poly)):
        for p in P:
            for i in range(len(Q)): d=min(d,segd(p,Q[i],Q[(i+1)%len(Q)]))
    return d
def clearance(S,dz=0.0,part='jaw',n=601):
    x,h=(2.9,3.05) if part=='jaw' else (2.05,2.55)
    return min(dist_poly_rect(hex_at(60.0*i/(n-1),dz),-x,x,S,S+h) for i in range(n))
if __name__=='__main__':
    # validation against dossier-v5 7.2 / review-r1 table (nominal peg height)
    for S,ref in((5.582,0.448),(5.088,0.104),(5.035,0.052),(4.631,0.0)):
        print('jaw S=%.3f computed %.3f dossier %.3f'%(S,clearance(S),ref))
    for S,ref in((5.582,1.025),(5.088,0.654),(4.631,0.318)):
        print('tongue S=%.3f computed %.3f dossier %.3f'%(S,clearance(S,0,'tongue'),ref))
    print('jaw peg +0.35, S=5.582: %.3f (review 0.193)'%clearance(5.582,0.35))
