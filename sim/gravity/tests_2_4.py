import json, numpy as np
from scipy.integrate import solve_ivp
c=299792458.0; GMs=1.32712440018e20; Rs=6.957e8; GMe=3.986004418e14; Re=6.371e6
out={}
# ---- Test 4: light bending by ray tracing through refractive index n = 1 + (1+gamma)*GM/(c^2 r)
def deflect(gamma, b=Rs):
    k=(1+gamma)*GMs/c**2
    def rhs(t,s):
        x,y,vx,vy=s; r=np.hypot(x,y)
        n=1+k/r; gx,gy=-k*x/r**3,-k*y/r**3   # grad n
        # ray eq: d/ds(n v) = grad n, with |v|=1 -> dv/ds = (grad n - (v.grad n) v)/n
        dot=vx*gx+vy*gy
        return [vx,vy,(gx-dot*vx)/n,(gy-dot*vy)/n]
    L=2000*Rs
    sol=solve_ivp(rhs,[0,2*L],[-L,b,1.0,0.0],rtol=1e-11,atol=1e-3,max_step=Rs)
    vx,vy=sol.y[2,-1],sol.y[3,-1]
    ang=-np.arctan2(vy,vx)
    # correct for finite path length: analytic tail beyond L adds (1+gamma)GM/(c^2 b)*(1 - cos) small; report both
    return ang*206264.806
out["light_bending_arcsec"]={"time_only_gamma0_numeric":deflect(0.0),"full_GR_gamma1_numeric":deflect(1.0),
    "time_only_formula":2*GMs/(c**2*Rs)*206264.806,"full_GR_formula":4*GMs/(c**2*Rs)*206264.806}
# ---- Test 2: clock slowing profile around Earth (uniform-density approximation)
s0=GMe/(c**2*Re)
def gr(r):  # r in Earth radii; fractional slowing vs far away
    return s0*(3-r*r)/2 if r<1 else s0/r
rows=[]
for r in np.round(np.concatenate([np.linspace(0,1,11),np.linspace(1.25,4.25,13)]),3):
    rows.append({"r_earth_radii":float(r),"gr_parts_per_1e10":gr(r)*1e10,"local_load_parts_per_1e10":(s0*1e10 if r<=1 else 0.0)})
out["reach_profile"]=rows
rgps=26560e3/Re
out["gps_gravity_part_us_per_day"]=(gr(1.0)-gr(rgps))*86400*1e6
out["hollow_shell_example"]={"shell":"Earth's mass in a thin shell of Earth's radius","clock_slowing_inside":s0,"pull_inside":0}
print(json.dumps(out,indent=1)); json.dump(out,open("results/tests_2_4.json","w"),indent=1)
