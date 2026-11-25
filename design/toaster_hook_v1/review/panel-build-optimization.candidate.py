w=param("panel_width",99)
h=param("panel_height",33)
t=param("panel_thickness",1.8)
r=param("panel_radius",8)
with BuildSketch(Plane.XZ) as sk:
    RectangleRounded(w,h,r)
panel=extrude(sk.sketch,amount=t)
panel=fillet(panel.faces().sort_by(Axis.Y)[0].edges(),0.5)
panel.color=srgb("#e5e8ec")
panel=scale(panel,by=param("panel_uniform_scale",0.625))
bore=param("panel_dial_axle_bore_mm",3.4)
cx=param("panel_dial_axis_x_mm",-18.75)
sweep=param("panel_dial_mark_sweep_deg",270)
start=param("panel_dial_mark_start_deg",225)
major_count=int(param("panel_dial_major_count",6))
minor_per_gap=int(param("panel_dial_minor_per_gap",4))
major_r=param("panel_dial_major_radius_mm",7.85)
number_r=param("panel_dial_number_radius_mm",9.5)
font_size=param("panel_dial_number_size_mm",2.4)
depth=param("panel_dial_engrave_depth_mm",0.25)
panel=panel-Pos(cx,0,0)*Rot(90,0,0)*Cylinder(bore/2,8)
from math import cos,sin,radians
with BuildSketch(Plane.XZ.offset(1.125-depth)) as marks:
    for ii in range(major_count):
        aa=start-sweep*ii/(major_count-1)
        theta=radians(aa)
        with Locations((cx+major_r*cos(theta),major_r*sin(theta))):
            Rectangle(0.6,1.0,rotation=aa-90)
        with Locations((cx+number_r*cos(theta),number_r*sin(theta))):
            Text(str(ii+1),font_size,font="Arial",font_style=FontStyle.BOLD)
        if ii<major_count-1:
            for jj in range(1,minor_per_gap+1):
                a2=start-sweep*(ii+jj/(minor_per_gap+1))/(major_count-1)
                with Locations((cx+7.75*cos(radians(a2)),7.75*sin(radians(a2)))):
                    Rectangle(0.5,0.65,rotation=a2-90)
gap=param("panel_inlay_clearance_mm",0.08)
# Fuse each translated 2D profile before extrusion. This is the exact
# union used by the original overlapping 3D cuts, with the same offsets.
def expanded_cutters(profile, offsets, amount):
    cutters=[]
    for face in profile.faces():
        copies=[Pos(dx,0,dz)*face for dx in offsets for dz in offsets]
        united=copies[0].fuse(*copies[1:])
        for merged_face in united.faces():
            cutters.append(extrude(merged_face,amount=amount,dir=(0,-1,0)))
    return cutters

socket=expanded_cutters(marks.sketch,[-gap,0,gap],depth+0.1)
panel=panel.cut(*socket)
retention_gap=param("panel_inlay_retention_pocket_clearance_mm",0.12)
front_web=param("panel_inlay_retention_web_mm",0.18)
retention_depth=param("panel_inlay_retention_pocket_depth_mm",0.24)
count=major_count
minor_count=minor_per_gap
with BuildSketch(Plane.XZ.offset(1.125-depth)) as lock_marks:
    for ii in range(count):
        aa=start-sweep*ii/(count-1)
        with Locations((cx+major_r*cos(radians(aa)),major_r*sin(radians(aa)))):
            Rectangle(0.6,1,rotation=aa-90)
        if ii<count-1:
            for jj in range(1,minor_count+1):
                a2=start-sweep*(ii+jj/(minor_count+1))/(count-1)
                with Locations((cx+7.75*cos(radians(a2)),7.75*sin(radians(a2)))):
                    Rectangle(0.5,0.65,rotation=a2-90)
pocket=expanded_cutters(
    Pos(0,front_web+retention_depth-depth,0)*lock_marks.sketch,
    [-retention_gap,-0.10,0,0.10,retention_gap],retention_depth)
panel=panel.cut(*pocket)
assert panel.is_valid
assert len(panel.solids())==1
label_size=param("panel_button_label_size_mm",1.8)
label_depth=param("panel_button_label_depth_mm",0.2)
label_z=param("panel_button_label_z_mm",3.525)
with BuildSketch(Plane.XZ.offset(1.125-label_depth)) as labels:
    for xx,label in [(0.625,"REHEAT"),(10.625,"CANCEL"),(20.625,"DEFROST")]:
        with Locations((xx,label_z)):
            Text(label,label_size,font="Arial",font_style=FontStyle.BOLD)
label_gap=param("panel_button_label_inlay_clearance_mm",0.06)
label_socket=expanded_cutters(labels.sketch,[-label_gap,0,label_gap],label_depth+0.1)
panel=panel.cut(*label_socket)
assert panel.is_valid and len(panel.solids())==1
button_seat_depth=param("panel_button_seat_depth_mm",0.35)
button_fit_gap=param("panel_button_fit_gap_mm",0.1)
button_seat_w=param("panel_button_seat_width_mm",6.875)
button_seat_h=param("panel_button_seat_height_mm",7.1875)
button_seat_r=param("panel_button_seat_corner_mm",2.34375)
button_key_w=param("panel_button_key_width_mm",4.8)
button_key_h=param("panel_button_key_height_mm",5.1125)
button_key_r=param("panel_button_key_corner_mm",1.4)
for xx in [0.625,10.625,20.625]:
    with BuildSketch(Plane.XZ.offset(1.125-button_seat_depth)) as seat_sk:
        with Locations((xx,-2.5)):
            RectangleRounded(button_seat_w+2*button_fit_gap,button_seat_h+2*button_fit_gap,button_seat_r+button_fit_gap)
    panel=panel-extrude(seat_sk.sketch,amount=button_seat_depth+0.1)
    with BuildSketch(Plane.XZ.offset(-0.1)) as key_sk:
        with Locations((xx,-2.5)):
            RectangleRounded(button_key_w+2*button_fit_gap,button_key_h+2*button_fit_gap,button_key_r+button_fit_gap)
    panel=panel-extrude(key_sk.sketch,amount=1.4)
assert panel.is_valid and len(panel.solids())==1
panel.color=srgb("#e5e8ec")
print("Major mark angles clockwise", [start-sweep*ii/(major_count-1) for ii in range(major_count)])
publish("panel",panel,"v42 英文与刻度嵌件面板",material="pla")
