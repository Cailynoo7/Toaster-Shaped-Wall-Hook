rx=param("eye_r_radius_x",3.1)
rz=param("eye_r_radius_z",3.9)
t=param("eye_r_thickness",0.5)
with BuildSketch(Plane.XZ) as sk:
    Ellipse(rx,rz)
s=extrude(sk.sketch,amount=t)
s.color=srgb("#45382c")
s=scale(s,by=param("eye_r_uniform_scale",0.625))
publish("eye_r",s,"v24 吐司眼睛",material="pla")
