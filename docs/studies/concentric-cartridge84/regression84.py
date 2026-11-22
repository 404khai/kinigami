"""Regression on the exploratory fixtures, not acceptance criteria."""
import json
def read(n):return json.load(open(n+'84.json'))
s=read('sphere');assert s['nominal_upper_diameter']<60
n=read('neighbor');assert len(n['sample_rows'])==45 and n['unresolved']==0 and n['yaw_angle_intervals_closed']>0
w=n['circumferential_fairings'];assert w['host_fairing_max_x']<w['guest_min_x_conservative'] and w['host_max_x']<w['guest_min_x']
p=read('phase-pairs');assert p['worst']['own flange | eject rear L730'][0]>39
l=read('local');assert abs(l['crosshead_shaft_min_x_gap']-1.94)<1e-9 and l['guide_nominal_radial_gap']>.119
sv=read('service')['rows'];assert sv['cell whole swept hulls']['overlap']==sv['cell lid full prism']['overlap']==[]
assert all(sv[tag+' M2 screw '+str(i)+' tool shank']['min_mesh_gap_mm']>.2 for tag in ('cell','pcb') for i in range(2))
r=read('rating');assert r['power_off']['dry residual']['max_selector_no_yoke_feedback_Nmm']>35
assert r['drives']['sleeve centered sensitivity']['guide_feedback']==0
assert r['cam']['minimum_centerline_curvature_R']>r['cam']['normal_groove_halfwidth']
assert len(read('installed')['parts'])>200 and read('mass')['as_built_upper'] is None
assert len(read('selector')['rows'])==3*147 and len(read('interval')['rows'])==27
assert read('witness')['common_ball_R']>=.60 and not any(r['unresolved_count'] for r in read('interval')['rows'])
assert all(not val['overlap'] for name,val in sv.items() if name.endswith('engaged bit'))
print('Take 84 exploratory regressions matched; installation rejected')
