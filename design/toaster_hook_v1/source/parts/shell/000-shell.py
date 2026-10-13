w=param("shell_width",120)
d=param("shell_depth",58)
h=param("shell_height",85)
t=param("shell_wall",3)
r=param("shell_corner",10)
sw=param("shell_slot_width",86)
sd=param("shell_slot_depth",20)
sy=param("shell_slot_y",-4)
top_r=param("shell_top_round",16)
front_add=param("shell_forward_extension",8)
bottom_add=param("shell_bottom_width_extra",8)
new_d=d+front_add
cy=-front_add/2
def section(zz,ww,dd,rr,yy):
    with BuildSketch(Plane.XY.offset(zz)) as sk:
        with Locations((0,yy)):
            RectangleRounded(ww,dd,rr)
    return sk.sketch
outer=loft([section(-h/2,w+bottom_add,new_d,r,cy),section(h/2,w,new_d,r,cy)],ruled=True)
outer=fillet(outer.faces().sort_by(Axis.Z)[-1].edges(),top_r)
inner_bottom=-h/2-1
inner_top=h/2-t
width_at=lambda zz:w+bottom_add*(h/2-zz)/h
inner=loft([section(inner_bottom,width_at(inner_bottom)-2*t,new_d-2*t,r-t,cy),section(inner_top,width_at(inner_top)-2*t,new_d-2*t,r-t,cy)],ruled=True)
inner=fillet(inner.faces().sort_by(Axis.Z)[-1].edges(),top_r-t)
shell=outer-inner
# The complete rear exterior is formed first, then split by one Y plane.
back_gap=param("shell_back_cap_gap",0.3)
split_y=param("shell_back_split_y",26)
rear_cut=Pos(0,split_y-back_gap/2+new_d/2,0)*Box(w+bottom_add+20,new_d,h+20)
shell=shell-rear_cut
with BuildSketch(Plane.XY.offset(h/2-5)) as sk:
    with Locations((0,sy)):
        RectangleRounded(sw,sd,4)
shell=shell-extrude(sk.sketch,amount=10)
with BuildSketch(Plane.YZ.offset(w/2-5)) as side:
    with Locations((-4,param("shell_handle_slot_z_reference",7.5))):
        SlotOverall(param("shell_handle_slot_height_reference",42.8),param("shell_handle_slot_width_reference",3.8),rotation=90)
shell=shell-extrude(side.sketch,amount=bottom_add+10)
shell.color=srgb("#fff9df")
shell=scale(shell,by=param("shell_uniform_scale",0.625))
# v26 physical dimensions, after the established overall scale.
frame_z=30.9375
base_raise=param("shell_base_raise_mm",4)
old_base_top=4.375
new_base_top=old_base_top+base_raise
shell=shell-Pos(0,0,new_base_top-frame_z-40)*Box(100,100,80)
back_snap_x=param("shell_back_snap_x_mm",32)
back_snap_z_low=param("shell_back_snap_z_low_mm",18)
back_snap_z_high=param("shell_back_snap_z_high_mm",36)
snap_gap=param("shell_snap_clearance_mm",0.2)
for sign in [-1,1]:
    for zz in [back_snap_z_low,back_snap_z_high]:
        receiver=Pos(sign*35.45,9.5,zz-frame_z)*Box(5.1,3,6.2)
        shell=shell+receiver
        pocket=Pos(sign*33.225,9.4,zz-frame_z)*Box(0.65,2.4,5.4)
        shell=shell-pocket
base_snap_x=param("shell_base_snap_x_mm",22)
for xx in [-base_snap_x,base_snap_x]:
    receiver=Pos(xx,-21.8625,10.425-frame_z)*Box(5.8,2.525,3.6)
    shell=shell+receiver
    shell=shell-Pos(xx,-20.875,10.425-frame_z)*Box(5.5,1.2,2.1)
shell.color=srgb("#fff9df")
dial_x=param("shell_dial_axis_x_mm",-18.75)
dial_z=param("shell_dial_axis_global_z_mm",20.875)
dial_bore=param("shell_dial_axle_bore_mm",3.4)
shell=shell-Pos(dial_x,-22,dial_z-frame_z)*Rot(90,0,0)*Cylinder(dial_bore/2,10)
shell.color=srgb("#fff9df")
button_key_w=param("shell_button_key_width_mm",4.8)
button_key_h=param("shell_button_key_height_mm",5.1125)
button_key_r=param("shell_button_key_corner_mm",1.4)
button_key_gap=param("shell_button_key_clearance_mm",0.1)
button_socket_depth=param("shell_button_socket_depth_mm",0.575)
button_center_z=param("shell_button_center_z_mm",18.375)
for xx in [0.625,10.625,20.625]:
    with BuildSketch(Plane.XZ.offset(23.125-button_socket_depth)) as key_sk:
        with Locations((xx,button_center_z-frame_z)):
            RectangleRounded(button_key_w+2*button_key_gap,button_key_h+2*button_key_gap,button_key_r+button_key_gap)
    shell=shell-extrude(key_sk.sketch,amount=button_socket_depth+0.1)
side_r=param("shell_side_socket_radius_mm",4.375)
side_gap=param("shell_side_socket_radial_clearance_mm",0.1)
side_depth=param("shell_side_socket_depth_mm",0.5)
side_x=param("shell_side_socket_origin_x_mm",40.83685350566157)
side_y=param("shell_side_socket_origin_y_mm",-2.5)
side_z=param("shell_side_socket_origin_z_mm",13.183758504072657)
side_angle=param("shell_side_socket_angle_deg",-2.6942842898561006)
side_socket=Pos(side_x,side_y,side_z-frame_z)*Rot(0,side_angle,0)*Pos(-1.25-(side_depth-0.1)/2,0,0)*Rot(0,90,0)*Cylinder(side_r+side_gap,side_depth+0.1)
shell=shell-side_socket
shell.color=srgb("#fff9df")
publish("shell",shell,"v38 联动拨柄行程槽机身",material="petg")
assert len(shell.solids())==1
print("Bread and case depth centre y mm",sy,cy,"front/rear y mm",-d/2-front_add,d/2)
