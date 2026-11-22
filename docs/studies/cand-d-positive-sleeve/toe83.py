"""A loaded finite-curvature point on the actual R1.50 entry, not the knot."""
from pull83 import *
def evaluate():
    out={}
    for shift in (0.,.20):
        b={}
        for i in range(3):
            for k,val in inside(shift,3.,i).items():
                if k not in b or val['F']>b[k]['F']:b[k]=dict(val,roller=i)
        out[str(shift)]=b
    return dict(label='exploratory',angle_deg=3,arc_past_knot=1.5*rad(3),center_lift=toe*(1-cos(rad(3))),cases=out)
if __name__=='__main__':print(json.dumps(evaluate(),indent=2))
