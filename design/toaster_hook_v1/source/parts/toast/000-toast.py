w=param("toast_width",80)
h=param("toast_height",77)
d=param("toast_depth",14)
arm=param("toast_arm",30)
drop=param("toast_bracket_drop",18)
pin=param("toast_slot_pin",6.4)
slotw=param("toast_slot_width",14)
rise=param("toast_crown_rise",22)
shoulder=param("toast_shoulder_height",47)
dip=param("toast_crown_dip",0.7/3)
notchw=param("toast_crown_dip_halfwidth",8/3)

rim=param("toast_crust_border",2)
from math import cos,sin,tan,acos,pi,sqrt
ry=param("toast_reference_crown_rise",19.7)
neck_ratio=param("toast_reference_neck_ratio",0.91)
rx=w/2
cz=h-ry
gain=param("toast_crown_soft_fullness",0.6)
curve_y=lambda aa:cz+ry*sin(aa)+gain*sin(aa)*cos(aa)**2
curve_dy=lambda aa:cos(aa)*(ry+gain*(1-3*sin(aa)**2))
theta=acos(neck_ratio)
left_neck=(-rx*neck_ratio,curve_y(-theta))
right_neck=(rx*neck_ratio,curve_y(-theta))
neck_dx=0.8*rx*sin(theta)/curve_dy(theta)
angles=[pi+theta,pi,3*pi/4,pi/2,pi/4,0,-theta]
side_bulge=param("toast_vertical_side_bulge",0.2)
# One mirrored quartic side: larger curvature near ends, smaller at mid-height.
side_shape=param("toast_side_curvature_bias",0.8)
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
            if abs(aa-pi/2)<1e-8:
                crown_controls=[p0,p1,p2,p3]
        Bezier(right_neck,(right_neck[0]-neck_dx,right_neck[1]-0.8),(w/2-5-side_slope,shoulder+1),(w/2-5,shoulder))
        Bezier(*list(reversed(side_right)))
        Bezier((w/2-5,5),(w/2-5-2*side_slope,3),(w/2-7,0),(w/2-10,0))
        Line((w/2-10,0),(-w/2+10,0))
        Bezier((-w/2+10,0),(-w/2+7,0),(-w/2+5+2*side_slope,3),(-w/2+5,5))
    make_face()
inner=Pos(0,0,rim)*scale(sk.sketch,by=((w-2*rim)/w,1,(h-2*rim)/h))
edge_round=param("toast_crust_edge_round",0.8)
groove_depth=param("toast_surface_groove_depth",0.55)
groove_halfwidth=param("toast_surface_groove_halfwidth",1.8)
groove_round=param("toast_surface_groove_round",1)
groove_radius=(groove_halfwidth**2+groove_depth**2)/(2*groove_depth)
def crown_point(tt,sx,sz,off):
    u=1-tt
    p=crown_controls
    xx=u**3*p[0][0]+3*u*u*tt*p[1][0]+3*u*tt*tt*p[2][0]+tt**3*p[3][0]
    zz=u**3*p[0][1]+3*u*u*tt*p[1][1]+3*u*tt*tt*p[2][1]+tt**3*p[3][1]
    dx=3*(u*u*(p[1][0]-p[0][0])+2*u*tt*(p[2][0]-p[1][0])+tt*tt*(p[3][0]-p[2][0]))*sx
    dz=3*(u*u*(p[1][1]-p[0][1])+2*u*tt*(p[2][1]-p[1][1])+tt*tt*(p[3][1]-p[2][1]))*sz
    length=sqrt(dx*dx+dz*dz)
    pp=(xx*sx,zz*sz+off)
    ff=(pp[0]+groove_round*dz/length,pp[1]-groove_round*dx/length)
    return pp,ff
def grooved_section(off):
    sx=(w-2*off)/w
    sz=(h-2*off)/h
    profile=Pos(0,0,off)*scale(sk.sketch,by=(sx,1,sz))
    apex=h-off
    cc=(0,apex+groove_radius-groove_depth)
    def error(tt):
        pp,ff=crown_point(tt,sx,sz,off)
        return (ff[0]-cc[0])**2+(ff[1]-cc[1])**2-(groove_radius+groove_round)**2
    left=0
    right=0.4
    assert error(left)<0 and error(right)>0
    for _ in range(60):
        mid=(left+right)/2
        if error(mid)>0: right=mid
        else: left=mid
    pp,ff=crown_point((left+right)/2,sx,sz,off)
    tt=(cc[0]+(ff[0]-cc[0])*groove_radius/(groove_radius+groove_round),cc[1]+(ff[1]-cc[1])*groove_radius/(groove_radius+groove_round))
    vx=(pp[0]-ff[0])+(tt[0]-ff[0])
    vz=(pp[1]-ff[1])+(tt[1]-ff[1])
    length=sqrt(vx*vx+vz*vz)
    mm=(ff[0]+groove_round*vx/length,ff[1]+groove_round*vz/length)
    assert abs(sqrt((pp[0]-ff[0])**2+(pp[1]-ff[1])**2)-groove_round)<1e-8
    with BuildSketch(Plane.XZ) as channel:
        with BuildLine():
            ThreePointArc((-pp[0],pp[1]),(-mm[0],mm[1]),(-tt[0],tt[1]))
            ThreePointArc((-tt[0],tt[1]),(0,apex-groove_depth),tt)
            ThreePointArc(tt,mm,pp)
            Line(pp,(pp[0],h+2))
            Line((pp[0],h+2),(-pp[0],h+2))
            Line((-pp[0],h+2),(-pp[0],pp[1]))
        make_face()
    return profile-channel.sketch
outer=extrude(grooved_section(0),amount=d/2-edge_round,both=True)
for sign in [-1,1]:
    sections=[]
    for fraction in [0,0.5,0.875,1]:
        off=edge_round*(1-sqrt(1-fraction*fraction))
        sections.append(Pos(0,sign*(d/2-edge_round+fraction*edge_round),0)*grooved_section(off))
    outer=outer+loft(sections)
bread=outer-extrude(inner,amount=d/2+1,both=True)
print("Groove lip circular section radius mm",groove_round)
bread.color=srgb("#d78f3a")
bread=scale(bread,by=param("toast_uniform_scale",0.625))
publish("toast",bread,"v24 周圈烘焙面包皮",material="pla")
assert len(bread.solids())==1
