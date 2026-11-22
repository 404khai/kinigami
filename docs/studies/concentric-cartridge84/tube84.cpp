// Prove X ordering of BOTH finite cover surfaces. Extrude each guest triangle
// toward +X past any host point, fatten in XY by a rigorous yaw-interval bound.
#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <vector>
using namespace std;
struct P{double x,y,z;};
P sub(P a,P b){return {a.x-b.x,a.y-b.y,a.z-b.z};}
P cross(P a,P b){return {a.y*b.z-a.z*b.y,a.z*b.x-a.x*b.z,a.x*b.y-a.y*b.x};}
double dot(P a,P b){return a.x*b.x+a.y*b.y+a.z*b.z;}
struct Tri{P p[3],e[3],n;double lo[3],hi[3],r;void prep(){
 for(int j=0;j<3;j++){e[j]=sub(p[(j+1)%3],p[j]);lo[j]=1e9;hi[j]=-1e9;}
 for(auto u:p){double w[]={u.x,u.y,u.z};for(int j=0;j<3;j++){lo[j]=min(lo[j],w[j]);hi[j]=max(hi[j],w[j]);}}
 n=cross(e[0],e[1]);}};
vector<Tri> H,G;double px,py,pitch,lift;long long tested=0;int accepted=0,unresolved=0;double maxwidth=0,minwidth=32;
bool separate(const Tri &h,const Tri &g,double d,P a){double sz=sqrt(dot(a,a));if(sz<1e-14)return false;
 double mn=1e90,mx=-1e90,gn=1e90,gx=-1e90;
 for(int i=0;i<3;i++){double t=dot(a,h.p[i]),v=dot(a,g.p[i]);mn=min(mn,t);mx=max(mx,t);gn=min(gn,v);gx=max(gx,v);}
 double f=d*(abs(a.x)+abs(a.y))+1e-9*sz;
 // Enclose all guest displacements [0,lift] and every point on each swept triangle.
 return mx<gn+min(0.,lift*a.x)-f || mn>gx+max(0.,lift*a.x)+f;}
bool check(double lo,double hi){double mid=-(lo+hi)*M_PI/360,c=cos(mid),s=sin(mid),dr=2*sin((hi-lo)*M_PI/720);
 P ex={1,0,0},ey={0,1,0};
 for(auto ref:G){Tri g=ref;
  for(auto &q:g.p){double x=q.x-px,y=q.y-py;q.x=px+pitch+c*x-s*y;q.y=py+s*x+c*y;}
  g.prep();double d=ref.r*dr+1e-9;
  for(const auto &h:H){if(h.hi[0]<g.lo[0]-d)break;if(h.lo[0]>g.hi[0]+lift+d||h.hi[1]<g.lo[1]-d||h.lo[1]>g.hi[1]+d||h.hi[2]<g.lo[2]-1e-9||h.lo[2]>g.hi[2]+1e-9)continue;
   tested++;bool sep=separate(h,g,d,h.n)||separate(h,g,d,g.n);
   for(auto u:g.e)if(!sep)sep=separate(h,g,d,cross(u,ex))||separate(h,g,d,cross(u,ey));
   for(auto u:h.e)if(!sep){sep=separate(h,g,d,cross(u,ex))||separate(h,g,d,cross(u,ey));for(auto v:g.e)if(!sep)sep=separate(h,g,d,cross(u,v));}
   if(!sep)return false;
  }
 }return true;}
void visit(double l,double r,int depth){if(check(l,r)){accepted++;minwidth=min(minwidth,r-l);maxwidth=max(maxwidth,r-l);}
 else if(depth==14){unresolved++;}else{double m=(l+r)/2;visit(l,m,depth+1);visit(m,r,depth+1);}}
int main(){int n;cin>>px>>py>>pitch>>lift>>n;for(int i=0;i<n;i++){Tri t{};for(auto &p:t.p){cin>>p.x>>p.y>>p.z;t.r=max(t.r,hypot(p.x-px,p.y-py));}t.prep();H.push_back(t);G.push_back(t);}
 sort(H.begin(),H.end(),[](auto&a,auto&b){return a.hi[0]>b.hi[0];});visit(-15,15,0);cout<<accepted<<" "<<unresolved<<" "<<tested<<" "<<minwidth<<" "<<maxwidth<<"\n";}
