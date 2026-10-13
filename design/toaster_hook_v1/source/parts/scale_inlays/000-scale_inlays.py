from math import cos,sin,radians
cx=param("scale_inlays_axis_x_mm",-18.75)
start=param("scale_inlays_start_deg",225)
sweep=param("scale_inlays_sweep_deg",270)
count=int(param("scale_inlays_major_count",6))
minor_count=int(param("scale_inlays_minor_per_interval",4))
major_r=param("scale_inlays_major_radius_mm",7.85)
number_r=param("scale_inlays_number_radius_mm",9.5)
font_size=param("scale_inlays_font_size_mm",2.4)
thickness=param("scale_inlays_thickness_mm",0.8)
back_y=param("scale_inlays_back_y_mm",-0.575)
lip=param("scale_inlays_retention_offset_mm",0.10)
lip_height=param("scale_inlays_retention_height_mm",0.2)
with BuildSketch(Plane.XZ.offset(-back_y)) as sk:
    for ii in range(count):
        aa=start-sweep*ii/(count-1)
        with Locations((cx+major_r*cos(radians(aa)),major_r*sin(radians(aa)))):
            Rectangle(0.6,1,rotation=aa-90)
        with Locations((cx+number_r*cos(radians(aa)),number_r*sin(radians(aa)))):
            Text(str(ii+1),font_size,font="Arial",font_style=FontStyle.BOLD)
        if ii<count-1:
            for jj in range(1,minor_count+1):
                a2=start-sweep*(ii+jj/(minor_count+1))/(count-1)
                with Locations((cx+7.75*cos(radians(a2)),7.75*sin(radians(a2)))):
                    Rectangle(0.5,0.65,rotation=a2-90)
parts=extrude(sk.sketch,amount=thickness)
# The narrow locking band sits in a wider internal pocket: 0.02 mm edge clearance,
# with 0.02 mm undercut beneath the socket mouth; no assembly material overlap.
with BuildSketch(Plane.XZ.offset(-back_y)) as lock_marks:
    for ii in range(count):
        aa=start-sweep*ii/(count-1)
        with Locations((cx+major_r*cos(radians(aa)),major_r*sin(radians(aa)))):
            Rectangle(0.6,1,rotation=aa-90)
        if ii<count-1:
            for jj in range(1,minor_count+1):
                a2=start-sweep*(ii+jj/(minor_count+1))/(count-1)
                with Locations((cx+7.75*cos(radians(a2)),7.75*sin(radians(a2)))):
                    Rectangle(0.5,0.65,rotation=a2-90)
band=extrude(Pos(0,-0.15,0)*lock_marks.sketch,amount=lip_height)
for dx in [-lip,0,lip]:
    for dz in [-lip,0,lip]:
        parts=parts+Pos(dx,0,dz)*band
assert parts.is_valid
parts.color=srgb("#63503a")
publish("scale_inlays",parts,"v28 刻度数字嵌件组",material="pla")
print("Separate physical inserts",len(parts.solids()))
assert len(parts.solids())==2*count+(count-1)*minor_count
