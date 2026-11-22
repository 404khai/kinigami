"""Numeric regression and mutual sanity checks; never a Gate or physical test."""
import json, math
from pathlib import Path
def load(n):return json.loads(Path(n+'83.json').read_text())
g=load('geo');k=g['hardened_sweep_proposal'];assert g['shaft_to_retained_shoulder']>.40 and g['old_closed_slot_front_remaining']<0 and k['new_window_reserve']>.025
assert min(k[n] for n in ['endwall_side_margin','edge_side_margin','blade_endwall_side_margin','blade_cheek_margin'])>.03
p=load('pull');b=load('band');c=load('ceiling')
for cap in ['tail45','cage45']:
 for case in ['service','table','fault']:
    key=cap+'_'+case;w=p['actual'][key]
    assert w['res']<1e-8 and w['F']<=b['loaded']['continuous_parallel_flat_upper'][key]<=c['parallel_common_offset_flat_land_upper_N'][key]
    assert max(b[i]['continuous_parallel_flat_upper'][key] for i in ['keyed_positive','keyed_negative'])<45
    assert p['reset_actual'][key]['F']<=b['reset']['continuous_parallel_flat_upper'][key]
r=load('retention'); assert r['extra_020']['vertices']==30 and r['extra_020']['V_reserve']>.15 and r['missing']['zero']['normals'][0]==0
h=load('pressure');assert 1290<h['actual_toe_hertz']['p']<1305 and min(r['normal_residual'] for r in h['pressures'])<1e-10
for u in h['pressures']:assert u['complementarity_mm']<2e-9 and u['normal_residual']<1e-10
e=load('exit');assert .0199<e['parked_cheek']['local_common_ball']['radius'] and e['parked_cheek']['pilot_clearance']>0 and e['roller_reserve']>.60
l=load('lock');assert l['minimum_local_curvature_radius']>.424 and .10<l['old_intersection']<.11 and l['conditional_pin_force']['45']['dry_raising_residual']['edge_projected_MPa_at_5um']>1000
u=load('cones')['contacts'];assert max(v['high'] for v in u.values())-max(v['low'] for v in u.values())<1e-6
print('Take 83 exploratory regression checks passed.')
