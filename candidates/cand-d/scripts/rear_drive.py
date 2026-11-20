"""v7 assembly stock and installation sections, mm. shutter_section models motion.
Gross stock deliberately overcharges intersecting pieces; volumes are upper
allocations, not claims that two solids can occupy the same material.
"""
from math import pi, hypot, sqrt
from shutter_section import R as R_SITE, B as R_BALL, HEAD, BALL_X

SPLIT_X = 23.35
NOSE_X = HEAD
EAR_X = 36.40
HEAD_PITCH = 37.25  # .35 clear beyond nose; no parasitic flange-to-flange clamp
TAIL_PITCH = -11.60
TAIL_MIN = TAIL_PITCH-(HEAD_PITCH-BALL_X+1.06+.04)
TAIL_R = 6.30
FLANGE_R = 8.0  # bounding circle only, lobes around 90/210/330; no disk this large below floor
BALL_SOURCE = 'https://sdballs.com/product/aisi-52100-chrome-steel-balls/'
PH,BR,SS,BS,CU=7810,7450,7900,7800,8900
def ring(ro,ri,length):
    assert 0<=ri<ro and length>0
    return pi*(ro**2-ri**2)*length

def stock(group):
    # Charge full plates where pockets are not deducted. The slim radius-6.30
    # section only extends to x35.60; keeper outer guides live forward of it.
    groups={
        'hub': [('rear hub OD5.7, broach inscribed diameter 3.4', ring(2.85,1.70,.63), PH)],
        'cartridge':[
            ('front of socket and floating tongue',ring(2.85,0,2.60),PH),
            ('rear annular retainer and front radial guide plate',ring(6.29,2.86,1.50),PH),
            ('split journals, shoulders and thrust faces',ring(5.8,3.8,2.40),BR),
            ('boxed hollow cam drum stock',ring(5.52,4.0,6.5),PH),
            ('driver disk and planar cam plate',ring(4.55,0,2.2),PH),
            ('three radial slides, two rails per station',6*4.8*.70*3.4,PH),
            ('fork heads, crossheads and followers',3*(2.6*2.5*.8+2.3*1.8*.8+ring(.55,0,2.5)),PH),
            ('stripper spider and its three pads',ring(4.9,1.5,.85)+3*(2*2*2.3),BS),
            ('stripper output guide rods and sleeves',3*ring(1.15,0,5.8),SS),
            ('hardened cheeks',6*1.7*1.0*1.85,BS),
            ('frame tie posts, lock stops, guide inserts and screws',6*2*1*7+8*ring(.75,0,3),PH),
            ('sensing leaves, pads, flex, screws and wire within cartridge',30.,CU)],
        'flange':[
            ('front guide plates and lateral ears',ring(6.30,2.1,.8)+2*3.8*5.2*.8,PH),
            ('three projecting station frames and nose guides',3*5.8*4.36*1.30,PH)],
        'tail':[
            ('flange and blind screw pads',ring(TAIL_R,0,1)+2*ring(1.5,0,.6),PH),
            ('three ball-carrying stems and radial necks',3*(2*2.1*3.6+1.6*1.5*1.45),PH),
            ('three crowned members',3*4*pi*1.06**3/3,BS)],
    }
    return groups[group]

def main():
    for g in ('hub','cartridge','flange','tail'):
        print(g,'mg upper',sum(v*d/1000 for _,v,d in stock(g)))
    print('outer axis range',TAIL_MIN,NOSE_X,'pitch',HEAD_PITCH-TAIL_PITCH)
    print('rear shaft gauged tip 25.35; rocker secured before axial insertion')
    print('Nominal 0.35 flange stand-off; permitted contact envelope must not consume it')
if __name__=='__main__':
    main()
