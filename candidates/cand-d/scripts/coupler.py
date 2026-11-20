"""cand-d v7 local unilateral contact screens. No physical qualification.
Run reciprocal.py (NumPy) for the full wrench and tolerances; shutter_section.py
for actuator work. Hertz applies only at an untruncated, smooth pole.
"""
import json, math
from pathlib import Path
from rear_drive import R_SITE, HEAD_PITCH, TAIL_PITCH
from shutter_section import pose

def hertz(f,r,e=210000/(2*(1-.30**2))):
    a=(3*f*r/(4*e))**(1/3)
    return a,3*f/(2*math.pi*a*a),a*a/r

def main():
    decl=json.loads((Path(__file__).resolve().parents[1]/'declaration.json').read_text())
    m=decl['mass_budget']['total_mass_mg']/1e6
    w=m*9.80665
    print(f'W {w:.4f} N; pitch {HEAD_PITCH-TAIL_PITCH:.2f} mm; 4W pull/push {4*w:.3f} N; bend {w*(HEAD_PITCH-TAIL_PITCH):.3f} N mm')
    # No assertion of equal sharing or Hertz allowance for an edge.
    for f in (14.44,25.34):
        a,p,d=hertz(f,1.04)
        print(f'{f:.2f} N smooth 52100 poles: patch r {a:.4f} mm, p0 {p:.1f} MPa, two-body indentation {d:.5f} mm')
    # A deliberately loose pocket cannot provide a preload merely by completing
    # the horizontal blade stroke. This admissible symmetric motion is enough
    # to disprove zero axial free travel at nominal build.
    print('nominal axial free travel',round(35.85-33.60-2*1.05,3),'mm')
    print('positive bearing overlap interrupted during keeper edge transit; no complete loaded release proof')
if __name__=='__main__':
    main()
