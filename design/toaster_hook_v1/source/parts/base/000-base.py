w=param("base_width",120)
d=param("base_depth",58)
t=param("base_thickness",7)
hw=param("base_hook_slot_width",12.6)
hd=param("base_hook_slot_depth",6.6)
hy=param("base_hook_slot_y",9)
front_add=param("base_forward_extension",8)
bottom_add=param("base_width_extra",8)
raise_mm=param("base_raise_mm",4)
# Extend the shell's exact width law down through the base.
shell_h=param("base_body_height_reference",85)
body_frame=param("base_body_center_z_mm",30.9375)
base_frame=2.1875
sc=param("base_uniform_scale",0.625)
corner=param("base_outer_corner_reference",10)
def width_at_global(z):
    return w+bottom_add*(shell_h/2-(z-body_frame)/sc)/shell_h
lower_z=-t/2
upper_z=t/2+raise_mm/sc
lower_w=width_at_global(lower_z*sc+base_frame)
upper_w=width_at_global(upper_z*sc+base_frame)
with BuildSketch(Plane.XZ.offset(front_add/2)) as outer_sk:
    Polygon((-lower_w/2,lower_z),(lower_w/2,lower_z),(upper_w/2,upper_z),(-upper_w/2,upper_z),align=None)
base=extrude(outer_sk.sketch,amount=(d+front_add)/2,both=True)
base=fillet([e for e in base.edges() if abs(e.tangent_at(0.5).Z)>0.9],corner)
base=fillet(base.faces().sort_by(Axis.Z)[0].edges(),param("base_bottom_edge_round",1.5))
base=base-Pos(0,hy,0)*Box(hw,hd,t+2*raise_mm/0.625+2)
base.color=srgb("#e9b371")
base=scale(base,by=param("base_uniform_scale",0.625))
frame_z=2.1875
base_top=4.375+raise_mm

# v32: one continuous recessed tray, same nominal wall as the case.
wall=param("base_tray_wall_mm",1.875)
tray_corner=param("base_tray_corner_mm",4.375)
# Parallel inner side planes keep the nominal normal wall thickness.
from math import sqrt
side_slope=bottom_add/(2*shell_h)
inner_width=lambda z:width_at_global(z)*sc-2*wall*sqrt(1+side_slope**2)
with BuildSketch(Plane.XZ.offset(front_add*sc/2)) as inner_sk:
    Polygon((-inner_width(wall)/2,wall-frame_z),(inner_width(wall)/2,wall-frame_z),(inner_width(base_top+1)/2,base_top+1-frame_z),(-inner_width(base_top+1)/2,base_top+1-frame_z),align=None)
cavity=extrude(inner_sk.sketch,amount=((d+front_add)*sc-2*wall)/2,both=True)
cavity=fillet([e for e in cavity.edges() if abs(e.tangent_at(0.5).Z)>0.9],tray_corner)
floor_round=param("base_inner_floor_round_mm",0.4)
cavity=fillet(cavity.faces().sort_by(Axis.Z)[0].edges(),floor_round)
base=base-cavity
snap_x=param("base_snap_x_mm",22)
snap_t=param("base_snap_beam_thickness_mm",1.2)
snap_len=param("base_snap_beam_length_mm",9.6)
snap_w=param("base_snap_width_mm",5)
hook_projection=param("base_snap_hook_projection_mm",0.7)
embed=param("base_snap_root_embed_mm",0.2)
tip=wall-embed+snap_len
assert 6<=snap_len/snap_t<=10
for xx in [-snap_x,snap_x]:
    beam=Pos(xx,-19.7,wall-embed+snap_len/2-frame_z)*Box(snap_w,snap_t,snap_len)
    beam=fillet(beam.edges().filter_by(Axis.Z),0.2)
    with BuildSketch(Plane.YZ.offset(xx-snap_w/2)) as latch_sk:
        Polygon((-20.3,tip-frame_z),(-20.3-hook_projection,tip-0.7-frame_z),(-20.3-hook_projection,tip-1.7-frame_z),(-20.3,tip-1.7-frame_z),align=None)
    latch=extrude(latch_sk.sketch,amount=snap_w)
    base=base+beam+latch
# Two rigid rear tongues slide below the back's retaining shoulders.
rear_x=param("base_rear_tongue_x_mm",29)
rear_w=param("base_rear_tongue_width_mm",5)
rear_t=param("base_rear_tongue_thickness_mm",1.2)
rear_top=param("base_rear_tongue_top_mm",10.2)
for xx in [-rear_x,rear_x]:
    root=Pos(xx,15.9,base_top-0.7-frame_z)*Box(rear_w,1.2,1.2)
    stem=Pos(xx,15.75,(base_top-1.2+rear_top)/2-frame_z)*Box(rear_w,0.9,rear_top-(base_top-1.2))
    tab=Pos(xx,15.5375,rear_top-rear_t/2-frame_z)*Box(rear_w,1.325,rear_t)
    base=base+root+stem+tab
release_w=param("base_release_slot_width_mm",3)
release_d=param("base_release_slot_depth_mm",1.2)
release_entry_y=param("base_release_entry_y_mm",-19.5)
release_tip_y=param("base_release_tip_y_mm",-21.1)
def release_section(xx,zz):
    yy=release_entry_y+(release_tip_y-release_entry_y)*zz/wall
    with BuildSketch(Plane.XY.offset(zz-frame_z)) as sk:
        with Locations((xx,yy)):
            Rectangle(release_w,release_d)
    return sk.sketch
for xx in [-snap_x,snap_x]:
    base=base-loft([release_section(xx,-0.1),release_section(xx,wall+0.2)],ruled=True)
foot_r=param("base_foot_socket_radius_mm",3.4375)
foot_gap=param("base_foot_socket_radial_clearance_mm",0.1)
foot_depth=param("base_foot_socket_depth_mm",0.5)
foot_x=param("base_foot_socket_x_mm",26.875)
foot_y_half=param("base_foot_socket_y_halfspan_mm",15.3125)
for xx in [-foot_x,foot_x]:
    for yy in [-2.5-foot_y_half,-2.5+foot_y_half]:
        base=base-Pos(xx,yy,(foot_depth-0.1)/2-frame_z)*Cylinder(foot_r+foot_gap,foot_depth+0.1)
base.color=srgb("#e9b371")
publish("base",base,"v36 光顺斜壁底座",material="petg")
assert len(base.solids())==1
print("Tray floor/walls",wall,"outer height",base_top,"continuous recess",base_top-wall,"snap tip",tip)
