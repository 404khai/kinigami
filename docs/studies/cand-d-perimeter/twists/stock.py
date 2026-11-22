"""Frozen Take 66 section, station x,y,t; mm/rad."""
from math import atan,asin,hypot,sqrt,cos,sin
B,K,KR,XB=14.54,.41,.26,-1.55
D,R0,R,C=12.42,2.45,2.50,-2.25
W,WC,RI,RO=3.20,3.26,1.10,1.16
MU=.23;M=hypot(1,K)
CORE_DISKS=[(C,7.60),(.20,7.10),(2.50,6.00),(4.40,3.50),
            (-.30,10.08-R),(2.25,9.00-R),(5.80,5.66-R)]
def b(x):return max(B+K*x,B+(K-KR)*XB+KR*x)
def w(x,t):return sqrt(b(x)**2-t*t)
h0=(12.75-.75*.60/.80-B)/(K+.60/.80)
h=h0+.24*(1/M-.80)/(.60+K/M);v=B+K*h0+.24;beta=atan(K)+asin(.60)
def rot(u,z,t,th):return (h+u*cos(th)+z*sin(th),v-u*sin(th)+z*cos(th),t)
