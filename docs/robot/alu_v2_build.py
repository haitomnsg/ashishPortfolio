# Builds "Alu" v2 - restyled for a stylized low-poly, sunlit sci-fi coast (the
# Caravan SandWitch-like direction): simple volumes, hard faceted edges, flat vertex
# colours on one matte material, chunky utilitarian gear, dust on the boots.
# The silhouette keeps v1 (inspo/Robot_One + Robot_Two): big screen head, ear disks,
# antenna, short blue limbs, heel wheels.
# Idempotent: rerunning removes and rebuilds the "Alu" and "Alu_Stage" collections.
# Run it from Blender's Scripting tab (Open -> Run Script). Tested on Blender 5.1.
#
# Materials: Alu_Paint (base colour = colour attribute "Col", matte), Alu_Screen,
# Alu_Glow. Three draw calls on the web.
# Rig: same empties as v1 (body, neck, head, antenna, arm_{L,R}_{1..3},
# leg_{L,R}_{1..3}, wheel_{L,R}); rotate them to pose. The robot faces -Y; L = +X.
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler

R = math.radians
SC = bpy.context.scene


# ---------------------------------------------------------------- reset
def purge_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        return
    for o in list(col.all_objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(col.children_recursive):
        bpy.data.collections.remove(c)
    bpy.data.collections.remove(col)


for n in ("Alu", "Alu_Stage"):
    purge_collection(n)
for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.lights, bpy.data.cameras):
    for d in list(coll):
        if d.users == 0:
            coll.remove(d)


def new_col(name):
    col = bpy.data.collections.new(name)
    SC.collection.children.link(col)
    return col


COL = new_col("Alu")
STAGE = new_col("Alu_Stage")


# ---------------------------------------------------------------- palette + materials
def lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


PAL = {
    "shell":  "#F6EAD6",  # warm cream shell (the game's #FFFCF7, sun-warmed)
    "blue":   "#2A9EE0",  # power blue limbs (between the game's #22A6E6 and site #0077B6)
    "dark":   "#2C2547",  # joints, soles: navy pushed toward the game's plum #36203D
    "dark2":  "#433B63",  # pack, lighter dark
    "orange": "#FF9F1C",  # gear: strap, pouch, pennant, ear ring
    "orange2": "#E0711A",  # pouch flap / shade of orange
    "olive":  "#5F7440",  # bedroll
    "metal":  "#B3B5C2",  # painted metal: fingers, collar, screws
    "dust":   "#C9A57E",  # dust on boots and wheels
}
DUST_H, DUST_MAX = 0.17, 0.55


def make_mat(name, hexc, rough=0.85, spec=0.3, vcol=False, emit=None, strength=0.0):
    old = bpy.data.materials.get(name)
    if old:
        bpy.data.materials.remove(old)
    m = bpy.data.materials.new(name)
    if m.node_tree is None:
        m.use_nodes = True
    nt = m.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(bsdf.outputs[0], out.inputs[0])
    I = bsdf.inputs
    I["Base Color"].default_value = lin(hexc)
    I["Roughness"].default_value = rough
    I["Specular IOR Level"].default_value = spec
    if vcol:
        vc = nt.nodes.new("ShaderNodeVertexColor")
        vc.layer_name = "Col"
        vc.location = (bsdf.location.x - 300, bsdf.location.y)
        nt.links.new(vc.outputs["Color"], I["Base Color"])
    if emit:
        I["Emission Color"].default_value = lin(emit)
        I["Emission Strength"].default_value = strength
    m.diffuse_color = lin(emit or hexc)
    return m


M = {
    "paint":  make_mat("Alu_Paint", "#FFFFFF", rough=0.86, spec=0.28, vcol=True),
    "screen": make_mat("Alu_Screen", "#15153A", rough=0.42, spec=0.5),
    "glow":   make_mat("Alu_Glow", "#DDF8FF", rough=0.5, emit="#7FE6FF", strength=2.2),
}


# ---------------------------------------------------------------- geometry helpers
PARENT = []  # (child, parent) - applied once all objects exist


def link_obj(name, data, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1),
             parent=None, col=None):
    o = bpy.data.objects.new(name, data)
    (col or COL).objects.link(o)
    o.location, o.rotation_euler, o.scale = loc, rot, scale
    if mat is not None and data is not None:
        data.materials.append(mat)
    if parent is not None:
        PARENT.append((o, parent))
    return o


def flat_mesh(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False
    return me


def paint(o, hexc, dust=True, jitter=0.025):
    """Flat vertex colour with a slight per-face variation (hand-coloured facets),
    blended toward dust near the ground (world z)."""
    rnd = random.Random(o.name)
    me = o.data
    attr = me.color_attributes.get("Col") or me.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    base = Vector(lin(hexc)[:3])
    dc = Vector(lin(PAL["dust"])[:3])
    mw = Matrix.LocRotScale(Vector(o.location), Euler(o.rotation_euler).to_quaternion(), Vector(o.scale))
    for poly in me.polygons:
        k = 1.0 + rnd.uniform(-jitter, jitter)
        for li in poly.loop_indices:
            t = 0.0
            if dust:
                z = (mw @ me.vertices[me.loops[li].vertex_index].co).z
                if z < DUST_H:
                    t = ((DUST_H - z) / DUST_H) ** 1.4 * DUST_MAX
            c = (base * k).lerp(dc, t)
            attr.data[li].color = (c.x, c.y, c.z, 1.0)


def add_bevel(o, width, segs=1, angle=None):
    b = o.modifiers.new("Bevel", "BEVEL")
    b.width = width
    b.segments = segs
    if angle is None:
        b.limit_method = "NONE"
    else:
        b.limit_method = "ANGLE"
        b.angle_limit = R(angle)
    b.harden_normals = False
    return b


def finish(o, color, mat, dust):
    if mat == "paint":
        paint(o, color, dust)
    return o


def box(name, loc, dims, color, parent, bevel=0.0, segs=2, top=(1, 1), bottom=(1, 1),
        rot=(0, 0, 0), mat="paint", dust=True):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        s = top if v.co.z > 0 else bottom
        v.co.x *= dims[0] * s[0]
        v.co.y *= dims[1] * s[1]
        v.co.z *= dims[2]
    o = link_obj(name, flat_mesh(bm, name), M[mat], loc, rot, parent=parent)
    if bevel > 0:
        add_bevel(o, bevel, segs)
    return finish(o, color, mat, dust)


def cyl(name, loc, r, depth, color, parent, r2=None, segs=10, rot=(0, 0, 0), bevel=None,
        bsegs=1, scale=(1, 1, 1), mat="paint", dust=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r,
                          radius2=(r if r2 is None else r2), depth=depth)
    o = link_obj(name, flat_mesh(bm, name), M[mat], loc, rot, scale, parent=parent)
    b = min(r, depth) * 0.22 if bevel is None else bevel
    if b > 0:
        add_bevel(o, b, bsegs, angle=40)
    return finish(o, color, mat, dust)


def ico(name, loc, r, color, parent, subdiv=1, scale=(1, 1, 1), mat="paint", dust=True):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    o = link_obj(name, flat_mesh(bm, name), M[mat], loc, (0, 0, 0), scale, parent=parent)
    return finish(o, color, mat, dust)


def ptube(name, pts, radius, color, parent, sides=6, mat="paint", dust=False):
    """Low-poly tube along world-space points (antenna, mouth)."""
    bm = bmesh.new()
    rings = []
    pts = [Vector(p) for p in pts]
    prev_n = None
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        if prev_n is None:
            up = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
            n1 = t.cross(up).normalized()
        else:  # parallel transport, so the tube does not twist
            n1 = (prev_n - t * prev_n.dot(t)).normalized()
        prev_n = n1
        n2 = t.cross(n1).normalized()
        rings.append([bm.verts.new(p + radius * (math.cos(2 * math.pi * k / sides) * n1 +
                                                 math.sin(2 * math.pi * k / sides) * n2))
                      for k in range(sides)])
    for a, b in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = link_obj(name, flat_mesh(bm, name), M[mat], parent=parent)
    return finish(o, color, mat, dust)


def joint(name, loc, parent=None, size=0.03):
    e = link_obj(name, None, loc=loc, parent=parent)
    e.empty_display_type = "SPHERE"
    e.empty_display_size = size
    return e


def arc(p0, p1, bow, n=8):
    """Points from p0 to p1 bulging by `bow` in the middle (cables)."""
    p0, p1, bow = Vector(p0), Vector(p1), Vector(bow)
    return [tuple(p0.lerp(p1, i / (n - 1)) + bow * math.sin(math.pi * i / (n - 1))) for i in range(n)]


def flag(name, hc, mdir, H, L, parent, fly=(-1, 0.15, 0), notch=0.28, amp=0.012, droop=0.02):
    """Swallowtail cloth pennant on a mast: faceted folds, cream hoist band + centre stripe."""
    f0 = Vector(fly).normalized()
    f = (f0 - mdir * f0.dot(mdir)).normalized()
    n = f.cross(mdir).normalized()
    us = (0.0, 0.13, 0.3, 0.48, 0.66, 0.84, 1.0)
    vs = (0.0, 0.36, 0.64, 1.0)
    bm = bmesh.new()
    grid = []
    for u in us:
        row = []
        for v in vs:
            lv = L * (1 - notch * (1 - abs(2 * v - 1)))
            hh = H * (1 - 0.32 * u)
            p = (hc + f * (u * lv) - mdir * ((v - 0.5) * hh + droop * u * u)
                 + n * (amp * math.sin(2 * math.pi * 0.9 * u + 0.4 + 0.8 * v) * (0.25 + 0.75 * u)))
            row.append(bm.verts.new(p))
        grid.append(row)
    cols = []
    for i in range(len(us) - 1):
        for j in range(len(vs) - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
            cols.append(PAL["shell"] if (i == 0 or j == 1) else PAL["orange"])
    me = flat_mesh(bm, name)
    o = link_obj(name, me, M["paint"], parent=parent)
    attr = me.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    for poly, hexc in zip(me.polygons, cols):
        for li in poly.loop_indices:
            attr.data[li].color = lin(hexc)
    sol = o.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.005
    sol.offset = 0
    return o


AX_X = (0, R(90), 0)  # cylinder axis along X
AX_Y = (R(90), 0, 0)  # cylinder axis along Y
C = PAL

# ---------------------------------------------------------------- rig (pivot empties)
root = joint("Alu_root", (0, 0, 0), size=0.12)
body = joint("body", (0, 0, 0.34), root, 0.08)
neck = joint("neck", (0, 0, 0.60), body)
head = joint("head", (0, 0, 0.64), neck, 0.06)
antenna = joint("antenna", (0.30, 0.04, 0.87), head)

arm, leg = {}, {}
for side, sx in (("L", 1), ("R", -1)):
    a1 = joint(f"arm_{side}_1", (0.20 * sx, 0, 0.555), body)
    a2 = joint(f"arm_{side}_2", (0.205 * sx, 0, 0.455), a1)
    a3 = joint(f"arm_{side}_3", (0.205 * sx, 0, 0.30), a2)
    l1 = joint(f"leg_{side}_1", (0.09 * sx, 0, 0.32), body)
    l2 = joint(f"leg_{side}_2", (0.095 * sx, 0, 0.225), l1)
    l3 = joint(f"leg_{side}_3", (0.095 * sx, 0, 0.085), l2)
    arm[side] = (a1, a2, a3)
    leg[side] = (l1, l2, l3)

# ---------------------------------------------------------------- head (big, like the game's cast)
HZ = 0.83
shell = box("Head_Shell", (0, 0, HZ), (0.54, 0.42, 0.40), C["shell"], head, bevel=0.06, segs=2, top=(0.97, 0.97))
cutter = box("Head_ScreenCutter", (0, -0.215, HZ - 0.005), (0.43, 0.07, 0.29), C["dark"], head, bevel=0.045, segs=2)
cutter.display_type = "WIRE"
cutter.hide_render = True
boo = shell.modifiers.new("ScreenRecess", "BOOLEAN")
boo.operation = "DIFFERENCE"
boo.solver = "EXACT"
boo.object = cutter

box("Head_Screen", (0, -0.192, HZ - 0.005), (0.41, 0.025, 0.27), C["dark"], head, bevel=0.04, segs=2, mat="screen")
for side, sx in (("L", 1), ("R", -1)):
    cyl(f"Eye_{side}", (0.088 * sx, -0.206, HZ + 0.005), 1.0, 1.0, C["shell"], head, segs=12, rot=AX_Y,
        bevel=0, scale=(0.046, 0.064, 0.008), mat="glow")
    for k, dz in enumerate((-0.026, 0.0, 0.026)):  # display scanlines
        box(f"Eye_{side}_Scan_{k}", (0.088 * sx, -0.2112, HZ + 0.005 + dz), (0.1, 0.002, 0.0045), C["dark"], head,
            mat="screen")
    for zt, zn in ((1, "T"), (-1, "B")):
        cyl(f"Screen_Screw_{side}{zn}", (0.178 * sx, -0.205, HZ - 0.005 + 0.105 * zt), 0.012, 0.008,
            C["orange"], head, segs=6, rot=AX_Y, bevel=0, dust=False)

# small smile
mouth_pts = [(0.024 * math.cos(R(a)), -0.209, HZ - 0.075 + 0.016 * math.sin(R(a))) for a in range(200, 341, 28)]
ptube("Mouth", mouth_pts, 0.0045, C["shell"], head, sides=4, mat="glow")

# ear disks: blue base, orange ring (Robot_One), shell cap
for side, sx in (("L", 1), ("R", -1)):
    cyl(f"Ear_{side}_Base", (0.283 * sx, 0.02, HZ - 0.01), 0.105, 0.036, C["blue"], head, segs=12, rot=AX_X, bevel=0.008)
    cyl(f"Ear_{side}_Ring", (0.303 * sx, 0.02, HZ - 0.01), 0.08, 0.012, C["orange"], head, segs=12, rot=AX_X, bevel=0.003)
    cyl(f"Ear_{side}_Cap", (0.31 * sx, 0.02, HZ - 0.01), 0.05, 0.016, C["shell"], head, segs=10, rot=AX_X, bevel=0.005)

# carry handle + top slot + a marking stripe
for sx in (1, -1):
    box(f"Handle_Post_{'L' if sx > 0 else 'R'}", (0.09 * sx, 0.05, 1.045), (0.024, 0.03, 0.05), C["dark"], head, bevel=0.005, segs=1)
box("Handle_Bar", (0, 0.05, 1.073), (0.21, 0.034, 0.024), C["dark"], head, bevel=0.006, segs=1)
box("Head_TopSlot", (-0.13, -0.12, 1.03), (0.10, 0.035, 0.012), C["blue"], head, bevel=0.004, segs=1)
box("Head_BackVent", (0, 0.211, HZ + 0.03), (0.22, 0.012, 0.1), C["dark"], head, bevel=0.008, segs=1)
for i, z in enumerate((-0.025, 0, 0.025)):
    box(f"Head_BackVent_Slat_{i}", (0, 0.218, HZ + 0.03 + z), (0.18, 0.006, 0.01), C["blue"], head, bevel=0.002, segs=1)
box("Head_Stripe",(0.155, -0.211, HZ + 0.172), (0.11, 0.006, 0.022), C["orange"], head, bevel=0.003, segs=1, dust=False)

# antenna from the left ear: straight rod, base housing, two collars, glowing tip
ant_pts = [(0.31, 0.04, 0.87), (0.316, 0.055, 0.99), (0.321, 0.072, 1.10), (0.324, 0.085, 1.19)]
ptube("Antenna_Rod", ant_pts, 0.0065, C["metal"], antenna, sides=6)
cyl("Antenna_Base", (0.31, 0.04, 0.872), 0.022, 0.034, C["dark"], antenna, segs=8)
cyl("Antenna_Collar_0", (0.313, 0.046, 0.93), 0.011, 0.012, C["dark"], antenna, segs=6, bevel=0)
cyl("Antenna_Collar_1", (0.318, 0.062, 1.04), 0.0105, 0.012, C["orange"], antenna, segs=6, bevel=0, dust=False)
ico("Antenna_Tip", (0.324, 0.086, 1.205), 0.022, C["shell"], antenna, subdiv=1, mat="glow")

# survey flag on a short roof mast (head top, rear right corner), like gear on a van roof:
# clamp block, beacon on top, swallowtail pennant flying back and out
MB, MT = Vector((-0.175, 0.12, 1.03)), Vector((-0.2, 0.17, 1.30))
mdir = (MT - MB).normalized()
mrot = mdir.to_track_quat("Z", "Y").to_euler()
box("Mast_Mount", (-0.175, 0.12, 1.042), (0.05, 0.05, 0.026), C["dark"], head, bevel=0.006, segs=1)
cyl("Mast_Mount_Bolt", (-0.175, 0.094, 1.042), 0.007, 0.006, C["metal"], head, segs=6, rot=AX_Y, bevel=0)
ptube("Mast", [tuple(MB), tuple(MB.lerp(MT, 0.5)), tuple(MT)], 0.0062, C["metal"], head, sides=6)
cyl("Mast_Collar", tuple(MB.lerp(MT, 0.12)), 0.011, 0.014, C["orange"], head, segs=6, rot=mrot, bevel=0, dust=False)
cyl("Mast_Beacon_Base", tuple(MT), 0.014, 0.022, C["dark"], head, segs=8, rot=mrot, bevel=0.003)
ico("Mast_Beacon", tuple(MT + mdir * 0.02), 0.014, C["shell"], head, subdiv=1, mat="glow")
FH, FL = 0.1, 0.19
hc = MB.lerp(MT, (1.2 - MB.z) / (MT.z - MB.z))
flag("Flag", hc, mdir, FH, FL, head, fly=(-1, 0.45, 0))
cyl("Flag_Sleeve", tuple(hc), 0.0095, FH + 0.012, C["shell"], head, segs=6, rot=mrot, bevel=0)
for k, nm in ((-1, "B"), (1, "T")):
    cyl(f"Flag_Ring_{nm}", tuple(hc + mdir * (k * (FH / 2 + 0.008))), 0.011, 0.006, C["dark"], head, segs=6,
        rot=mrot, bevel=0)

# ---------------------------------------------------------------- neck + torso
# neck bellows (rubber accordion) on a metal collar
for i, z in enumerate((0.606, 0.621, 0.636, 0.651)):
    cyl(f"Neck_Bellow_{i}", (0, 0, z), 0.05 if i % 2 == 0 else 0.042, 0.016, C["dark"], neck, segs=10, bevel=0.004)
cyl("Neck_Collar", (0, 0, 0.598), 0.064, 0.014, C["metal"], neck, segs=10, bevel=0.003)

box("Chest", (0, 0, 0.50), (0.32, 0.24, 0.20), C["shell"], body, bevel=0.045, segs=2, bottom=(0.88, 1.0))
box("Chest_Seam", (0, -0.121, 0.505), (0.236, 0.008, 0.146), C["dark"], body, bevel=0.012, segs=1)
box("Chest_Plate", (0, -0.126, 0.505), (0.226, 0.01, 0.136), C["shell"], body, bevel=0.01, segs=1)
for i, (bx, bz) in enumerate(((-0.098, 0.56), (0.098, 0.56), (-0.098, 0.45), (0.098, 0.45))):
    cyl(f"Chest_Bolt_{i}", (bx, -0.132, bz), 0.008, 0.006, C["metal"], body, segs=6, rot=AX_Y, bevel=0)
box("Chest_Panel", (-0.035, -0.133, 0.525), (0.1, 0.008, 0.055), C["dark"], body, bevel=0.006, segs=1)
for i, x in enumerate((-0.06, -0.035, -0.01)):
    box(f"Chest_Light_{i}", (x, -0.138, 0.525), (0.013, 0.005, 0.03), C["shell"], body, bevel=0.002, segs=1, mat="glow")
cyl("Chest_Button", (0.058, -0.134, 0.525), 0.018, 0.01, C["orange"], body, segs=8, rot=AX_Y, bevel=0.003, dust=False)
for i, z in enumerate((0.466, 0.476, 0.486)):  # speaker slots
    box(f"Chest_Slot_{i}", (0.045, -0.132, z), (0.06, 0.004, 0.0045), C["dark"], body)

# docked power pack: housing, orange lid, charge meter (3 of 4 lit), vents, two cells
for i, z in enumerate((0.555, 0.445)):
    box(f"Pack_Dock_{i}", (0, 0.128, z), (0.15, 0.03, 0.026), C["dark"], body, bevel=0.005, segs=1)
box("Pack", (0, 0.178, 0.50), (0.23, 0.10, 0.20), C["shell"], body, bevel=0.024, segs=2, top=(0.94, 0.92))
box("Pack_Lid", (0, 0.178, 0.603), (0.19, 0.08, 0.012), C["orange"], body, bevel=0.004, segs=1, dust=False)
box("Pack_Inset", (0, 0.229, 0.495), (0.17, 0.008, 0.14), C["dark"], body, bevel=0.008, segs=1)
for i, z in enumerate((0.445, 0.47, 0.495, 0.52)):
    box(f"Pack_Charge_{i}", (-0.045, 0.234, z), (0.05, 0.005, 0.014), C["dark2"], body, bevel=0.002, segs=1,
        mat="glow" if i < 3 else "paint")
for i, x in enumerate((0.015, 0.035, 0.055)):
    box(f"Pack_Vent_{i}", (x, 0.234, 0.49), (0.01, 0.006, 0.09), C["metal"], body, bevel=0.002, segs=1)
for side, sx in (("L", 1), ("R", -1)):
    cyl(f"Pack_Cell_{side}", (0.132 * sx, 0.178, 0.5), 0.032, 0.16, C["metal"], body, segs=10, bevel=0.006)
    for z, nm in ((0.425, "B"), (0.575, "T")):
        cyl(f"Pack_Cell_{side}_Cap{nm}", (0.132 * sx, 0.178, z), 0.035, 0.018, C["dark"], body, segs=10, bevel=0.004)
    cyl(f"Pack_Cell_{side}_Band", (0.132 * sx, 0.178, 0.5), 0.034, 0.02, C["blue"], body, segs=10, bevel=0.003)
    # power cable from the cell to the shoulder servo
    ptube(f"Cable_{side}", arc((0.125 * sx, 0.15, 0.57), (0.2 * sx, 0.03, 0.56), (0.035 * sx, 0, 0.012)),
          0.0085, C["dark"], body, sides=6)
    cyl(f"Cable_{side}_Plug", (0.125 * sx, 0.152, 0.57), 0.014, 0.022, C["metal"], body, segs=6, bevel=0,
        rot=(R(90), 0, R(-35 * sx)))

for i, z in enumerate((0.378, 0.394, 0.41, 0.426)):  # waist bellows
    cyl(f"Waist_Bellow_{i}", (0, 0, z), 0.105 if i % 2 == 0 else 0.092, 0.016, C["dark"], body, segs=10,
        scale=(1, 0.75, 1), bevel=0.004)
box("Pelvis", (0, 0, 0.345), (0.22, 0.16, 0.075), C["blue"], body, bevel=0.022, segs=2)
for side, sx in (("L", 1), ("R", -1)):
    cyl(f"Pelvis_Cap_{side}", (0.113 * sx, 0, 0.345), 0.026, 0.008, C["metal"], body, segs=8, rot=AX_X, bevel=0)

# ---------------------------------------------------------------- arms (chunky, Robot_Two)
for side, sx in (("L", 1), ("R", -1)):
    a1, a2, a3 = arm[side]
    x = 0.205 * sx
    ico(f"Shoulder_{side}", (0.20 * sx, 0, 0.555), 0.045, C["dark"], a1)
    box(f"Shoulder_{side}_Pad", (0.215 * sx, 0, 0.578), (0.09, 0.115, 0.07), C["shell"], a1, bevel=0.022, segs=2)
    cyl(f"Shoulder_{side}_Servo", (0.262 * sx, 0, 0.572), 0.028, 0.008, C["metal"], a1, segs=8, rot=AX_X, bevel=0)
    cyl(f"Shoulder_{side}_Bolt", (0.267 * sx, 0, 0.572), 0.009, 0.006, C["dark"], a1, segs=6, rot=AX_X, bevel=0)
    cyl(f"UpperArm_{side}", (x, 0, 0.50), 0.028, 0.09, C["dark"], a1, segs=8)
    ico(f"Elbow_{side}", (x, 0, 0.455), 0.035, C["dark"], a2)
    cyl(f"Forearm_{side}", (x, 0, 0.385), 0.066, 0.13, C["blue"], a2, r2=0.048, segs=10, bevel=0.012)
    cyl(f"Forearm_{side}_Cuff", (x, 0, 0.316), 0.054, 0.016, C["dark"], a2, segs=10, bevel=0.003)
    cyl(f"Forearm_{side}_Glow", (x, 0, 0.327), 0.0515, 0.005, C["shell"], a2, segs=10, bevel=0, mat="glow")
    ico(f"Palm_{side}", (x, 0, 0.285), 1.0, C["dark"], a3, scale=(0.036, 0.042, 0.033))
    for fy, fn in ((-1, "F"), (1, "B")):
        box(f"Finger_{side}{fn}", (x, 0.024 * fy, 0.25), (0.03, 0.019, 0.06), C["metal"], a3, bevel=0.006, segs=1,
            rot=(R(-14 * fy), 0, 0))

# ---------------------------------------------------------------- legs (short, chunky boots)
for side, sx in (("L", 1), ("R", -1)):
    l1, l2, l3 = leg[side]
    x = 0.095 * sx
    ico(f"Hip_{side}", (0.09 * sx, 0, 0.32), 0.042, C["dark"], l1)
    cyl(f"Thigh_{side}", (x, 0, 0.275), 0.034, 0.08, C["dark"], l1, segs=8)
    box(f"Knee_{side}", (x, -0.014, 0.228), (0.10, 0.11, 0.07), C["shell"], l2, bevel=0.02, segs=2)
    cyl(f"Knee_{side}_Servo", (0.147 * sx, -0.014, 0.228), 0.022, 0.008, C["metal"], l2, segs=8, rot=AX_X, bevel=0)
    cyl(f"Knee_{side}_Bolt", (0.151 * sx, -0.014, 0.228), 0.008, 0.006, C["dark"], l2, segs=6, rot=AX_X, bevel=0)
    box(f"Piston_{side}_Mount", (x, 0.042, 0.305), (0.022, 0.04, 0.016), C["dark"], l1, bevel=0.003, segs=1)
    cyl(f"Piston_{side}_Sleeve", (x, 0.058, 0.272), 0.013, 0.07, C["dark2"], l1, segs=8, bevel=0.003)
    cyl(f"Piston_{side}_Rod", (x, 0.058, 0.215), 0.006, 0.075, C["metal"], l2, segs=6, bevel=0)
    box(f"Shin_{side}", (x, 0.0, 0.15), (0.125, 0.135, 0.12), C["blue"], l2, bevel=0.022, segs=2, top=(0.88, 0.88))
    cyl(f"Ankle_{side}", (x, 0, 0.088), 0.032, 0.03, C["dark"], l3, segs=8)
    box(f"Boot_{side}", (x, -0.028, 0.056), (0.135, 0.205, 0.07), C["shell"], l3, bevel=0.022, segs=2, top=(0.92, 0.9))
    box(f"Boot_{side}_Strap", (x, -0.07, 0.088), (0.14, 0.032, 0.012), C["orange"], l3, bevel=0.003, segs=1)
    box(f"Sole_{side}", (x, -0.028, 0.0175), (0.128, 0.198, 0.035), C["dark"], l3, bevel=0.008, segs=1)
    wx = 0.168 * sx
    cyl(f"wheel_{side}", (wx, 0.062, 0.036), 0.036, 0.03, C["dark"], l3, segs=10, rot=AX_X, bevel=0.007)
    cyl(f"wheel_{side}_Hub", (wx + 0.014 * sx, 0.062, 0.036), 0.016, 0.008, C["orange"], l3, segs=6, rot=AX_X, bevel=0)

# ---------------------------------------------------------------- parenting
bpy.context.view_layer.update()
for child, par in PARENT:
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()
try:
    cutter.hide_set(True)
except Exception:
    pass

# ---------------------------------------------------------------- hero pose (zero the empties for rest)
head.rotation_euler = (R(-5), R(6), R(16))      # curious tilt toward camera
antenna.rotation_euler = (R(-6), 0, 0)
for side, sx in (("L", 1), ("R", -1)):
    a1, a2, a3 = arm[side]
    a1.rotation_euler = (R(4), R(-10 * sx), 0)
    a2.rotation_euler = (R(-22), 0, 0)
arm["L"][2].rotation_euler = (0, 0, R(20))
arm["R"][0].rotation_euler = (R(-25), R(100), 0)  # wave
arm["R"][1].rotation_euler = (0, R(48), 0)
arm["R"][2].rotation_euler = (0, R(10), R(-30))

# ---------------------------------------------------------------- stage: sunlit limestone, sky
GROUND = "#DCC8A6"
stage_mat = make_mat("Stage_Stone", "#FFFFFF", rough=0.95, spec=0.2, vcol=True)


def stage_obj(name, me, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    return link_obj(name, me, stage_mat, loc, rot, scale, col=STAGE)


def stage_paint(o, hexc, jitter=0.0, seed=0):
    rnd = random.Random(seed)
    me = o.data
    attr = me.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    base = Vector(lin(hexc)[:3])
    for p in me.polygons:  # per-face jitter = hand-coloured facets
        k = 1.0 + rnd.uniform(-jitter, jitter)
        for li in p.loop_indices:
            attr.data[li].color = (base.x * k, base.y * k, base.z * k, 1.0)


bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=24, y_segments=24, size=9.0)
rnd = random.Random(4)
for v in bm.verts:
    d = Vector((v.co.x, v.co.y)).length
    if d > 1.6:
        v.co.z = rnd.uniform(0, 0.12) * min(1.0, (d - 1.6) / 3)
ground = stage_obj("Ground", flat_mesh(bm, "Ground"))
stage_paint(ground, GROUND, 0.06, 1)


def rock(name, loc, r, scale, seed, hexc="#E9DCC4"):
    rr = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
    for v in bm.verts:
        v.co *= rr.uniform(0.8, 1.15)
        if v.co.z < 0:
            v.co.z *= 0.3
    o = stage_obj(name, flat_mesh(bm, name), loc, (0, 0, rr.uniform(0, 6.28)), scale)
    stage_paint(o, hexc, 0.07, seed)
    return o


rock("Rock_A", (-1.15, 1.2, 0.05), 0.45, (1.5, 1.1, 0.75), 11)
rock("Rock_B", (1.3, 2.4, 0.0), 0.7, (1.6, 1.2, 0.9), 12)
rock("Rock_C", (0.62, -0.2, 0.0), 0.12, (1.3, 1.0, 0.7), 13)

# sun + sky
sun_d = bpy.data.lights.new("Sun", "SUN")
sun_d.energy = 4.2
sun_d.angle = R(6)
sun_d.color = lin("#FFE3BC")[:3]
sun = link_obj("Sun", sun_d, col=STAGE)
sun.rotation_euler = (Vector((0, 0, 0)) - Vector((-2.2, -1.4, 2.6))).to_track_quat("-Z", "Y").to_euler()

w = bpy.data.worlds.get("Alu_World") or bpy.data.worlds.new("Alu_World")
if w.node_tree is None:
    try:
        w.use_nodes = True
    except Exception:
        pass
nt = w.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld")
mix = nt.nodes.new("ShaderNodeMixShader")
lp = nt.nodes.new("ShaderNodeLightPath")
amb = nt.nodes.new("ShaderNodeBackground")       # what the scene is lit by
amb.inputs[0].default_value = lin("#9DB4EA")  # blue-violet shadows
amb.inputs[1].default_value = 0.42
sky = nt.nodes.new("ShaderNodeBackground")       # what the camera sees: a vertical gradient
sky.inputs[1].default_value = 1.0
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.35
ramp.color_ramp.elements[0].color = lin("#CFEAF7")
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = lin("#3FA2DE")
nt.links.new(tc.outputs["Window"], sep.inputs[0])
nt.links.new(sep.outputs["Y"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], sky.inputs[0])
nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
nt.links.new(amb.outputs[0], mix.inputs[1])
nt.links.new(sky.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs[0])
SC.world = w

# camera: 3/4 front, slightly low, like the hero
cd = bpy.data.cameras.new("Alu_Cam")
cd.lens = 72
cam = link_obj("Alu_Cam", cd, loc=(1.55, -2.85, 0.78), col=STAGE)
cam.rotation_euler = (Vector((0.0, 0, 0.6)) - cam.location).to_track_quat("-Z", "Y").to_euler()
SC.camera = cam

# render: EEVEE, sharp stylized colour
SC.render.engine = "BLENDER_EEVEE"
SC.render.resolution_x = 1200
SC.render.resolution_y = 1500
SC.render.resolution_percentage = 100
SC.eevee.taa_render_samples = 64
for attr, val in (("use_raytracing", True), ("use_shadows", True), ("shadow_ray_count", 2),
                  ("shadow_step_count", 10), ("use_fast_gi", True)):
    try:
        setattr(SC.eevee, attr, val)
    except Exception:
        pass
vs = SC.view_settings
vs.view_transform = "Standard"
vs.look = "None"
vs.exposure = 0.0

# soft bloom on the emissives only
ng = bpy.data.node_groups.get("Alu_Comp") or bpy.data.node_groups.new("Alu_Comp", "CompositorNodeTree")
ng.nodes.clear()
for item in list(ng.interface.items_tree):
    ng.interface.remove(item)
ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
rl = ng.nodes.new("CompositorNodeRLayers")
gl = ng.nodes.new("CompositorNodeGlare")
gout = ng.nodes.new("NodeGroupOutput")
for v in ("Bloom", "BLOOM"):
    try:
        gl.inputs["Type"].default_value = v
        break
    except Exception:
        pass
gl.inputs["Threshold"].default_value = 1.0
gl.inputs["Strength"].default_value = 0.35
gl.inputs["Size"].default_value = 0.4
ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
ng.links.new(gl.outputs[0], gout.inputs[0])
SC.compositing_node_group = ng
SC.render.use_compositing = True

for n in ("Cube", "Light", "Camera"):
    o = bpy.data.objects.get(n)
    if o:
        o.hide_render = True
        try:
            o.hide_set(True)
        except Exception:
            pass

bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in COL.all_objects:
    if o.type == "MESH" and not o.hide_render:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        o.evaluated_get(dg).to_mesh_clear()
result = {"objects": len(COL.all_objects), "tris": tris}
