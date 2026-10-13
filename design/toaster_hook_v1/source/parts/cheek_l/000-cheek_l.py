rx=param("cheek_l_radius_x",4.8)
rz=param("cheek_l_radius_z",4.6)
t=param("cheek_l_thickness",0.5)
with BuildSketch(Plane.XZ) as sk:
    Ellipse(rx,rz)
s=extrude(sk.sketch,amount=t)
s.color=srgb("#f7cda9")
s=scale(s,by=param("cheek_l_uniform_scale",0.625))
publish("cheek_l",s,"v24 吐司腮红",material="pla")
