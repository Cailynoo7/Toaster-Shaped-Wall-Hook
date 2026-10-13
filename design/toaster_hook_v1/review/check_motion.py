"""Read-only sampled motion audit of the published v42 STEP (no CAD build/export)."""
import math
import json
from itertools import combinations
from pathlib import Path
from build123d import Axis, Location, import_step

ROOT = Path(__file__).resolve().parents[3]
EXPECTED_REVISION = "d8735744031ab13899df4952f81c33fe33167766bf2919ebdc7ec3e0a5058865"
receipts = [p for p in (ROOT / "manufacturing/toaster_hook_v1/releases").glob("*/receipt.json")
            if json.loads(p.read_text())["revision"] == EXPECTED_REVISION and (p.parent / "model.step").exists()]
assert receipts, "Missing published v42 STEP"
receipt = max(receipts, key=lambda p: json.loads(p.read_text())["generatedAt"])
STEP = receipt.parent / "model.step"
parts = {s.label: s for s in import_step(str(STEP)).children}
ANGLE = 34.51810784
ARM = 18.75
PIVOT_Z = 21.875
fixed = ("shell", "back", "base", "slot_trim", "panel", "dial", "dial_cap", "collar")
moving = ("toast", "crumb", "hook", "side_handle", "lever")
same_assembly = {frozenset(("toast", "crumb")), frozenset(("hook", "side_handle"))}

def disjoint_boxes(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    return any(getattr(aa.max, i) <= getattr(bb.min, i) + 1e-7 or getattr(bb.max, i) <= getattr(aa.min, i) + 1e-7 for i in ("X", "Y", "Z"))

assert len(parts) == 29
assert sum(len(s.solids()) for s in parts.values()) == 78
checks = 0
for sample in range(17):
    angle = -ANGLE + 2 * ANGLE * sample / 16
    rise = ARM * math.sin(math.radians(angle))
    poses = dict(parts)
    for name in ("toast", "crumb"):
        poses[name] = parts[name].moved(Location((0, 0, rise - 10.625)))
    for name in ("hook", "side_handle"):
        poses[name] = parts[name].moved(Location((0, 0, 10.625 - rise)))
    poses["lever"] = parts["lever"].rotate(Axis((0, 10, PIVOT_Z), (0, 1, 0)), angle - ANGLE)
    pairs = [(a, b) for a in moving for b in fixed]
    pairs += [p for p in combinations(moving, 2) if frozenset(p) not in same_assembly]
    for a, b in pairs:
        if disjoint_boxes(poses[a], poses[b]):
            continue
        common = poses[a].intersect(poses[b])
        volume = 0 if common is None else common.volume
        assert volume < 1e-5, f"Collision at {angle:.8f} degrees: {a}/{b}, {volume:.6f} mm3"
        checks += 1
    print(f"pose {sample + 1}/17: angle={angle:.5f}, toast={33.125 + rise:.5f}, hook={PIVOT_Z - rise:.5f}: clear", flush=True)

# Exact pin horizontal excursion across the entire angular interval: the
# horizontal centreline of the rounded slot is +/-2.375 mm; pin R1.875,
# slot end R2.0 gives a further 0.125 mm radial allowance.
pin_min_x = ARM * math.cos(math.radians(ANGLE))
pin_max_x = ARM
slot_center_x = 16.875
assert pin_min_x >= slot_center_x - 2.375
assert pin_max_x <= slot_center_x + 2.375
print(f"pin centre x=[{pin_min_x:.6f}, {pin_max_x:.6f}], slot centreline x=[14.5, 19.25]: clear")

# Solid-volume mass estimates only: actual sliced infill and friction are not
# represented. Densities are disclosed engineering defaults, not measurements.
toast_names = ("toast", "crumb", "eye_l", "eye_r", "cheek_l", "cheek_r", "smile")
toast_mass_g = sum(parts[n].volume for n in toast_names) / 1000 * 1.24
hook_mass_g = parts["hook"].volume / 1000 * 1.27 + parts["side_handle"].volume / 1000 * 1.24
print(f"exact Boolean checks={checks}; solid PLA toast estimate={toast_mass_g:.3f} g; PETG hook + PLA side handle={hook_mass_g:.3f} g")
assert toast_mass_g > hook_mass_g
print("PASS: sampled sweep and analytic pin range; physical return/load tests remain required")

for degrees in (0, 45, 90, 135, 180, 225, 270, 315):
    dial = parts["dial"].rotate(Axis((-18.75, -26.0125, 20.875), (0, 1, 0)), degrees)
    cap = parts["dial_cap"].rotate(Axis((-18.75, -26.0125, 20.875), (0, 1, 0)), degrees)
    for name in ("shell", "panel", "dial_rim", "base", "back"):
        for shape in (dial, cap):
            if disjoint_boxes(shape, parts[name]):
                continue
            common = shape.intersect(parts[name])
            assert common is None or common.volume < 1e-5, f"Dial collision: {degrees} degrees/{name}"
    print(f"dial rotation +{degrees} degrees: clear", flush=True)
print("PASS: eight sampled dial rotations; printed bearing fit/glue remain untested")
