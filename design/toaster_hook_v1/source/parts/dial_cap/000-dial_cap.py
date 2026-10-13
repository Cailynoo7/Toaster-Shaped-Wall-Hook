od=param("dial_cap_outer_diameter_mm",6)
depth=param("dial_cap_thickness_mm",1.6)
bore=param("dial_cap_bore_mm",3.2)
socket_depth=param("dial_cap_socket_depth_mm",1.2)
s=Rot(90,0,0)*Cylinder(od/2,depth)
s=s-Pos(0,-depth/2+socket_depth/2-0.05,0)*Rot(90,0,0)*Cylinder(bore/2,socket_depth+0.1)
s.color=srgb("#e9b371")
publish("dial_cap",s,"v27 旋钮内侧止退帽",material="petg")
assert len(s.solids())==1
