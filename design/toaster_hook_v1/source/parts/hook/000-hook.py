w=param("hook_width",12)
t=param("hook_stem_thickness",5)
length=param("hook_length",87)
slotw=param("hook_slot_width",14)
pind=param("hook_slot_height",6.4)
# Input follower lives behind lever; front hook stem clears pivot and toast.
s=Pos(27,15.5,0)*Box(18,5,12)
s=s+Pos(27,15.5,6)*Box(10,5,12)
s=s+Pos(27,7.75,12)*Box(10,20.5,6)
s=s+Pos(15,0,12)*Box(42,t,6)
# J profile in YZ. Local y=0 means assembly y=6.5.
with BuildSketch(Plane.YZ) as sk:
    with BuildLine():
        Polyline((-t/2,12),(t/2,12),(t/2,-length+4))
        ThreePointArc((t/2,-length+4),(-12,-length-9),(-26,-length+4))
        Line((-26,-length+4),(-27,-length+12))
        ThreePointArc((-27,-length+12),(-24,-length+15),(-21,-length+12))
        Line((-21,-length+12),(-20,-length+4))
        ThreePointArc((-20,-length+4),(-12,-length-2),(-t/2,-length+4))
        Line((-t/2,-length+4),(-t/2,12))
    make_face()
j=extrude(sk.sketch,amount=w/2,both=True)
edge_round=param("hook_edge_round",2.4)
j=fillet(j.edges(),edge_round)
s=s+j
with BuildSketch(Plane.XZ.offset(-15.5)) as sl:
    with Locations((27,0)):
        SlotOverall(slotw,pind)
s=s-extrude(sl.sketch,amount=5,both=True)
s.color=srgb("#f2f2eb")
s=scale(s,by=param("hook_uniform_scale",0.625))
# Side actuator link, in this moving hook's physical-mm frame.
link_root_x=param("hook_side_link_root_x_mm",21)
link_end_x=param("hook_side_link_end_x_mm",34.5)
link_y=param("hook_side_link_y_mm",4.5)
link_width=param("hook_side_link_width_mm",2.5)
link_thick=param("hook_side_link_thickness_mm",3)
handle_y=param("hook_side_handle_y_mm",-2.5)
handle_z_offset=param("hook_side_handle_z_offset_mm",13.75)
bridge_z=7.5
hook_origin_y=4.0625
arm=Pos((link_root_x+link_end_x)/2,link_y-hook_origin_y,bridge_z)*Box(link_end_x-link_root_x,link_thick,link_thick)
riser=Pos(link_end_x,link_y-hook_origin_y,(bridge_z+handle_z_offset)/2)*Box(link_width,link_thick,handle_z_offset-bridge_z+link_thick)
top=Pos(link_end_x,(link_y+handle_y)/2-hook_origin_y,handle_z_offset)*Box(link_width,link_y-handle_y+link_thick,link_thick)
socket_size=param("hook_side_socket_outer_mm",4.4)
socket_key_y=param("hook_side_socket_key_y_mm",2)
socket_key_z=param("hook_side_socket_key_z_mm",1.875)
socket_gap=param("hook_side_socket_key_gap_mm",0.1)
socket_depth=param("hook_side_socket_depth_mm",1.6)
socket=Pos(link_end_x,handle_y-hook_origin_y,handle_z_offset)*Box(link_width,socket_size,socket_size)
s=s+arm+riser+top+socket
socket_right=link_end_x+link_width/2
s=s-Pos(socket_right-socket_depth/2+0.05,handle_y-hook_origin_y,handle_z_offset)*Box(socket_depth+0.1,socket_key_y+2*socket_gap,socket_key_z+2*socket_gap)
s.color=srgb("#f2f2eb")
publish("hook",s,"v42 大圆角联动挂钩",material="petg")
assert len(s.solids())==1
