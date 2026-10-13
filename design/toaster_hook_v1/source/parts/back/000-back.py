w=param("back_width",120)
d=param("back_depth",58)
h=param("back_height",85)
t=param("back_thickness",2.7)
shaft=param("back_shaft_diameter",6)
guide_gap=param("back_guide_clearance",0.5)
guide_depth=param("back_guide_depth",7.3)
top_r=param("back_top_round",16)
front_add=param("back_forward_extension",8)
bottom_add=param("back_bottom_width_extra",8)
corner=param("back_corner",10)
back_gap=param("back_cap_gap",0.3)
split_y=param("back_split_y",26)
new_d=d+front_add
cy=-front_add/2
def section(zz,ww):
    with BuildSketch(Plane.XY.offset(zz)) as sk:
        with Locations((0,cy)):
            RectangleRounded(ww,new_d,corner)
    return sk.sketch
# Same complete body exterior as shell, including taper and all rear rounds.
outer=loft([section(-h/2,w+bottom_add),section(h/2,w)],ruled=True)
outer=fillet(outer.faces().sort_by(Axis.Z)[-1].edges(),top_r)
s=outer & Pos(0,split_y+back_gap/2+new_d/2,0)*Box(w+bottom_add+20,new_d,h+20)
cap=s
base_raise=param("back_base_raise_mm",4)
# lip joins cap; 0.3mm perimeter gap to shell cavity
lip=Pos(0,25.75,0)*Box(100,1.5,52)
lip=fillet(lip.edges().filter_by(Axis.Y),5)
s=s+lip
# rear channel guides and endpoint stop shoulders
guide_outer=27+9+guide_gap+1.5
# Parameterized side clearance at the follower shoulders
for x in [-guide_outer,-(54-guide_outer),54-guide_outer,guide_outer]:
    s=s+Pos(x,23.15,-14.5)*Box(3,guide_depth,46)
stop_inner_half=param("back_upper_stop_opening_halfwidth",6)
stop_height=param("back_upper_stop_height",6)
column_outer=guide_outer+1.5
stop_outer_half=column_outer-27
stop_width=stop_outer_half-stop_inner_half
stop_offset=(stop_outer_half+stop_inner_half)/2
for x in [-27,27]:
    s=s+Pos(x,23.15,-40)*Box(18,guide_depth,5)
    for sign in [-1,1]:
        s=s+Pos(x+sign*stop_offset,23.15,11.5)*Box(stop_width,guide_depth,stop_height)
print("Upper stop shoulder width mm",stop_width*0.625,"opening mm",2*stop_inner_half*0.625,"outer aligned span mm",2*stop_outer_half*0.625)
# integral custom pivot; global centre z=35, shaft occupies y10.5..26.8
s=s+Pos(0,18.65,-14.5)*Rot(90,0,0)*Cylinder(shaft/2,16.3)
s.color=srgb("#fff9df")
sc=param("back_uniform_scale",0.625)
s=scale(s,by=sc)
cap=scale(cap,by=sc)
frame_z=30.9375
# Trim rear skin after scaling the fully connected original mechanism.
s=s-Pos(0,26.34375,4.375+base_raise-frame_z-40)*Box(100,20,80)
stop_bridge_w=param("back_stop_bridge_width_mm",16)
for xx in [-16.875,16.875]:
    s=s+Pos(xx,16.25,8.25-frame_z)*Box(stop_bridge_w,1.2,2.5)
snap_x=param("back_snap_x_mm",32)
snap_z_low=param("back_snap_z_low_mm",18)
snap_z_high=param("back_snap_z_high_mm",36)
snap_t=param("back_snap_beam_thickness_mm",1.2)
snap_len=param("back_snap_beam_length_mm",8.2)
snap_width=param("back_snap_width_mm",5)
hook_projection=param("back_snap_hook_projection_mm",0.7)
assert 6<=snap_len/snap_t<=10
for sign in [-1,1]:
    for zz in [snap_z_low,snap_z_high]:
        beam=Pos(sign*snap_x,16.6-snap_len/2,zz-frame_z)*Box(snap_t,snap_len,snap_width)
        beam=fillet(beam.edges().filter_by(Axis.Y),0.2)
        root=Pos(sign*snap_x,16.45,zz-frame_z)*Box(2,0.7,snap_width+1)
        with BuildSketch(Plane.XY.offset(zz-frame_z-snap_width/2)) as latch_sk:
            Polygon((sign*(snap_x+snap_t/2),8.4),(sign*(snap_x+snap_t/2+hook_projection),9.1),(sign*(snap_x+snap_t/2+hook_projection),10.4),(sign*(snap_x+snap_t/2),10.4),align=None)
        latch=extrude(latch_sk.sketch,amount=snap_width)
        s=s+beam+root+latch
rear_x=param("back_base_tongue_x_mm",29)
rear_w=param("back_base_tongue_width_mm",5)
rear_gap=param("back_base_tongue_clearance_mm",0.2)
rear_tab_top=param("back_base_tongue_top_mm",10.2)
rear_shoulder_t=param("back_base_shoulder_thickness_mm",1.2)
for xx in [-rear_x,rear_x]:
    s=s+Pos(xx,15.5375,rear_tab_top+rear_gap+rear_shoulder_t/2-frame_z)*Box(rear_w+0.4,2.325,rear_shoulder_t)
# Stop feet stay inside the tray; the continuous rear wall stays uncut.
tray_inner_rear=param("back_base_inner_rear_mm",16.25)
tray_clearance=param("back_base_wall_clearance_mm",0.2)
tray_top=param("back_base_outer_top_mm",8.375)
# Protect the exterior above its mating plane; cut clearance only in the internals.
cap=cap-Pos(0,0,tray_top-frame_z-40)*Box(100,100,80)
internal_relief=Pos(0,tray_inner_rear-tray_clearance+10,tray_top+tray_clearance-frame_z-40)*Box(54,20,80)
s=s-(internal_relief-cap)
s.color=srgb("#fff9df")
publish("back",s,"v40 底沿贴齐背板",material="petg")
assert len(s.solids())==1, [(so.volume, tuple(so.bounding_box().min), tuple(so.bounding_box().max)) for so in s.solids()]
