rx=param("cheek_r_radius_x",4.8)
rz=param("cheek_r_radius_z",4.6)
t=param("cheek_r_thickness",0.5)
with BuildSketch(Plane.XZ) as sk:
    Ellipse(rx,rz)
s=extrude(sk.sketch,amount=t)
s.color=srgb("#f7cda9")
s=scale(s,by=param("cheek_r_uniform_scale",0.625))
publish("cheek_r",s,"v24 吐司腮红",material="pla")
