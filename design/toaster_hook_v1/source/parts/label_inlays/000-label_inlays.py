size=param("label_inlays_font_size_mm",1.8)
thickness=param("label_inlays_thickness_mm",0.8)
back_offset=param("label_inlays_back_offset_mm",0.575)
zz=param("label_inlays_center_z_mm",3.525)
xx0=param("label_inlays_start_x_mm",0.625)
step=param("label_inlays_word_spacing_mm",10)
with BuildSketch(Plane.XZ.offset(back_offset)) as sk:
    for ii,label in enumerate(["REHEAT","CANCEL","DEFROST"]):
        with Locations((xx0+ii*step,zz)):
            Text(label,size,font="Arial",font_style=FontStyle.BOLD)
s=extrude(sk.sketch,amount=thickness)
s.color=srgb("#594132")
publish("label_inlays",s,"v33 三组英文字母嵌件",material="pla")
assert s.is_valid and len(s.solids())==19
print("Independent glyphs",len(s.solids()),"thickness",thickness,"proud",back_offset+thickness-1.125)
