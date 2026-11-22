"""Regression of the rejected trial; not a physical test or a Gate."""
import json,hashlib
from math import isclose
def read(x):return json.load(open(x))
def yes(c):assert c
h=read('local82.json');r=read('rating82.json');s=read('sphere82.json');m=read('mass82.json');a=read('service82.json')['tests'];n=read('neighbor82.json')['rows'];w=read('witness82.json')
yes(hashlib.sha256(open('upstream80.json','rb').read()).hexdigest()=='5eff474c69bc789ace3623c367cd4218248074a7d1b0b9cb160e78e48dde28e1')
yes(s['common_diameter_upper_mm']<60)
yes(h['analytic_draw_witness']['radius_mm']<min(h['analytic_draw_witness']['clearances'].values()))
yes(max(row[2] for row in h['variant'])>.5 and max(row[3] for row in h['variant'])>.3)
yes(w['eject_at_axis']['analytic_ball_radius']<min(w['eject_at_axis']['margins']))
yes(len(n)==45 and len(read('phase-pairs.json')['rows'])==45)
yes(all(q['largest_five'] for q in n if q['phase']=='LOCK'))
yes(44.8<r['force_cap']['conditional_jammed_reset_max_N']<45)
yes(r['guide']['0.23']['required_unlock_push_N'] is None)
yes(r['thread_hold']['mu_threshold_square']>0.05)
yes(a['rear sleeve into empty barrel']['continuous_polygon_gap_lower_mm']>.024)
yes(a['sleeve after fixed eject bushes']['worst_sample_intersection_mm3']>0)
yes(a['uncoupled rear M3 screw WITH flange after thrust housing']['worst_sample_intersection_mm3']>0)
yes(m['as_built_mass_upper_g'] is None and m['as_built_COM'] is None)
print('Take 82 rejected layout: regression assertions passed (exploratory).')
