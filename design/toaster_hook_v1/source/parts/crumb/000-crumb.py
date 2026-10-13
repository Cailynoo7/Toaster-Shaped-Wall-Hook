w=param("crumb_outer_width",80)
h=param("crumb_outer_height",77)
d=param("crumb_thickness",14)
rise=param("crumb_crown_rise",22)
shoulder=param("crumb_outer_shoulder",47)
rim=param("crumb_border",2)
gap=param("crumb_crust_clearance",0.15)
dip=param("crumb_crown_dip",0.4)
notchw=param("crumb_crown_dip_halfwidth",2)
drop=param("crumb_bracket_drop",18)
pin=param("crumb_slot_pin",6.4)
slotw=param("crumb_slot_width",14)
from math import cos,sin,tan,acos,pi,sqrt
ry=param("crumb_reference_crown_rise",19.7)
neck_ratio=param("crumb_reference_neck_ratio",0.91)
rx=w/2
cz=h-ry
gain=param("crumb_crown_soft_fullness",0.6)
curve_y=lambda aa:cz+ry*sin(aa)+gain*sin(aa)*cos(aa)**2
curve_dy=lambda aa:cos(aa)*(ry+gain*(1-3*sin(aa)**2))
theta=acos(neck_ratio)
left_neck=(-rx*neck_ratio,curve_y(-theta))
right_neck=(rx*neck_ratio,curve_y(-theta))
neck_dx=0.8*rx*sin(theta)/curve_dy(theta)
angles=[pi+theta,pi,3*pi/4,pi/2,pi/4,0,-theta]
side_bulge=param("crumb_vertical_side_bulge",0.2)
# One mirrored quartic side: larger curvature near ends, smaller at mid-height.
side_shape=param("crumb_side_curvature_bias",0.8)
side_span=shoulder-5
side_slope=side_bulge*(4+side_shape)/side_span
side_right=[(w/2-5+side_bulge*bb,5+side_span*ii/4) for ii,bb in enumerate([0,(4+side_shape)/4,(4-side_shape)/3,(4+side_shape)/4,0])]
side_left=[(-xx,zz) for xx,zz in side_right]
assert 0<=side_shape<=1.5
def side_x(tt):
    return w/2-5+side_bulge*(4*tt*(1-tt)+side_shape*tt*(1-tt)*(1-2*tt)**2)
assert abs(side_x(0.5)-(w/2-5+side_bulge))<1e-9
assert max(side_x(ii/200) for ii in range(201))<=w/2-5+side_bulge+1e-9
print("Mirrored side peak x mm",side_x(0.5),"side end/mid curvature per mm",side_bulge*(8+10*side_shape)/side_span**2/(1+side_slope**2)**1.5,side_bulge*(8-2*side_shape)/side_span**2)
with BuildSketch(Plane.XZ) as sk:
    with BuildLine():
        Bezier(*side_left)
        Bezier((-w/2+5,shoulder),(-w/2+5+side_slope,shoulder+1), (left_neck[0]+neck_dx,left_neck[1]-0.8),left_neck)
        for aa,bb in zip(angles,angles[1:]):
            p0=(rx*cos(aa),curve_y(aa))
            p3=(rx*cos(bb),curve_y(bb))
            k=4/3*tan((bb-aa)/4)
            p1=(p0[0]-k*rx*sin(aa),p0[1]+k*curve_dy(aa))
            p2=(p3[0]+k*rx*sin(bb),p3[1]-k*curve_dy(bb))
            Bezier(p0,p1,p2,p3)
        Bezier(right_neck,(right_neck[0]-neck_dx,right_neck[1]-0.8),(w/2-5-side_slope,shoulder+1),(w/2-5,shoulder))
        Bezier(*list(reversed(side_right)))
        Bezier((w/2-5,5),(w/2-5-2*side_slope,3),(w/2-7,0),(w/2-10,0))
        Line((w/2-10,0),(-w/2+10,0))
        Bezier((-w/2+10,0),(-w/2+7,0),(-w/2+5+2*side_slope,3),(-w/2+5,5))
    make_face()
inner=Pos(0,0,rim+gap)*scale(sk.sketch,by=((w-2*rim-2*gap)/w,1,(h-2*rim-2*gap)/h))
cream=extrude(inner,amount=d/2,both=True)
# The moving follower is integral to the cream bread core.
cream=cream+Pos(-27,26,-drop)*Box(18,5,12)
cream=cream+Pos(-27,26,-6.5)*Box(10,5,25)
bridge_z=param("crumb_bridge_z",6)
cream=cream+Pos(-27,13,bridge_z)*Box(10,26,6)
with BuildSketch(Plane.XZ.offset(-26)) as sl:
    with Locations((-27,-drop)):
        SlotOverall(slotw,pin)
cream=cream-extrude(sl.sketch,amount=6,both=True)
cream.color=srgb("#fff9e3")
cream=scale(cream,by=param("crumb_uniform_scale",0.625))
publish("crumb",cream,"v24 米色面包主体与滑块",material="pla")
assert len(cream.solids())==1
