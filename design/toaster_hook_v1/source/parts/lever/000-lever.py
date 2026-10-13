import math
arm=param("lever_arm",30)
t=param("lever_thickness",5)
bh=param("lever_beam_height",8)
bore=param("lever_bore_diameter",6.4)
pin=param("lever_pin_diameter",6)
angle=param("lever_angle_deg",34.51810784)
s=Box(2*arm,t,bh)
s=s+Rot(90,0,0)*Cylinder(6,t)
for x in [-arm,arm]:
    s=s+Pos(x,0,0)*Rot(90,0,0)*Cylinder(bh/2,t)
    s=s+Pos(x,4.4,0)*Rot(90,0,0)*Cylinder(pin/2,6)
s=s-Rot(90,0,0)*Cylinder(bore/2,t+2)
s=Rot(0,angle,0)*s
s.color=srgb("#dc8a4e")
s=scale(s,by=param("lever_uniform_scale",0.625))
publish("lever",s,"v24 等臂杠杆",material="petg")
print("arm travel mm",2*arm*math.sin(math.radians(abs(angle))))
assert len(s.solids())==1
