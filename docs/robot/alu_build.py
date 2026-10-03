# Builds "Alu" - a chibi robot mixing inspo/Robot_One (boxy screen head, cream shell,
# slate joints, heel wheels) and inspo/Robot_Two (glowing eyes, ear disks, antenna,
# glossy blue limbs), coloured with the portfolio palette from docs/DESIGN.md.
# Idempotent: rerunning removes and rebuilds the "Alu" and "Alu_Stage" collections.
# Run it from Blender's Scripting tab (Open -> Run Script). Tested on Blender 5.1.
#
# Rig: every part is parented to an empty at its joint (body, neck, head, antenna,
# arm_{L,R}_{1..3}, leg_{L,R}_{1..3}); rotate the empties to pose, zero them for the
# rest pose. Heel wheels wheel_{L,R} spin on their local Z. The robot faces -Y; L = +X.
import bpy, bmesh, math
from mathutils import Vector

R = math.radians
SC = bpy.context.scene


# ---------------------------------------------------------------- reset
def purge_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        return
    for o in list(col.all_objects):
        data = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if data is not None and data.users == 0:
            for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.lights, bpy.data.cameras):
                if coll.get(data.name) == data:
                    coll.remove(data)
                    break
    for c in list(col.children_recursive):
        bpy.data.collections.remove(c)
    bpy.data.collections.remove(col)


for n in ("Alu", "Alu_Stage"):
    purge_collection(n)


def new_col(name):
    col = bpy.data.collections.new(name)
    SC.collection.children.link(col)
    return col


COL = new_col("Alu")
STAGE = new_col("Alu_Stage")


# ---------------------------------------------------------------- colour + materials
def lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def make_mat(name, hexc, rough=0.5, metal=0.0, coat=0.0, coat_rough=0.08,
             emit=None, strength=0.0):
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
    I["Metallic"].default_value = metal
    I["Coat Weight"].default_value = coat
    I["Coat Roughness"].default_value = coat_rough
    if emit:
        I["Emission Color"].default_value = lin(emit)
        I["Emission Strength"].default_value = strength
    m.diffuse_color = lin(emit or hexc)
    return m


M = {
    "shell":  make_mat("Alu_Shell",  "#F3F7FA", rough=0.38, coat=0.35),           # satin white
    "ocean":  make_mat("Alu_Ocean",  "#0077B6", rough=0.32, coat=0.6),            # glossy blue paint
    "joint":  make_mat("Alu_Joint",  "#1A2150", rough=0.55),                      # navy joints
    "rubber": make_mat("Alu_Rubber", "#11142C", rough=0.85),                      # soles, tyres
    "metal":  make_mat("Alu_Metal",  "#B9CCD6", rough=0.28, metal=1.0),           # brushed metal
    "screen": make_mat("Alu_Screen", "#0A1A52", rough=0.12, coat=1.0, coat_rough=0.03,
                       emit="#0D3C8C", strength=0.22),                            # face screen
    "glow":   make_mat("Alu_Glow",   "#00B4D8", rough=0.3, emit="#00B4D8", strength=6.0),
    "eye":    make_mat("Alu_Eye",    "#E6FBFF", rough=0.3, emit="#CFF6FF", strength=9.0),
    "sky":    make_mat("Alu_Sky",    "#90E0EF", rough=0.35, coat=0.4),
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


def finish_mesh(bm, name, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return me


def add_bevel(o, width, segs=5, angle=None):
    b = o.modifiers.new("Bevel", "BEVEL")
    b.width = width
    b.segments = segs
    if angle is None:
        b.limit_method = "NONE"
    else:
        b.limit_method = "ANGLE"
        b.angle_limit = R(angle)
    b.harden_normals = True
    return b


def rbox(name, loc, dims, bevel, mat, parent, segs=5, top=(1, 1), bottom=(1, 1), rot=(0, 0, 0)):
    """Rounded box. top/bottom scale the upper/lower verts in x,y for tapering."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= dims[0]
        v.co.y *= dims[1]
        v.co.z *= dims[2]
        s = top if v.co.z > 0 else bottom
        v.co.x *= s[0]
        v.co.y *= s[1]
    o = link_obj(name, finish_mesh(bm, name), mat, loc, rot, parent=parent)
    add_bevel(o, bevel, segs)
    return o


def cyl(name, loc, r, depth, mat, parent, r2=None, segs=48, rot=(0, 0, 0), bevel=None,
        bsegs=3, scale=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r,
                          radius2=(r if r2 is None else r2), depth=depth)
    o = link_obj(name, finish_mesh(bm, name), mat, loc, rot, scale, parent=parent)
    add_bevel(o, bevel if bevel is not None else min(r, depth) * 0.25, bsegs, angle=30)
    return o


def sph(name, loc, r, mat, parent, scale=(1, 1, 1), rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
    return link_obj(name, finish_mesh(bm, name), mat, loc, rot, scale, parent=parent)


def torus(name, loc, Rmaj, rmin, mat, parent, rot=(0, 0, 0), seg=64, ring=12):
    bm = bmesh.new()
    rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        rv = []
        for j in range(ring):
            b = 2 * math.pi * j / ring
            rr = Rmaj + rmin * math.cos(b)
            rv.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), rmin * math.sin(b))))
        rings.append(rv)
    for i in range(seg):
        for j in range(ring):
            bm.faces.new((rings[i][j], rings[(i + 1) % seg][j],
                          rings[(i + 1) % seg][(j + 1) % ring], rings[i][(j + 1) % ring]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link_obj(name, finish_mesh(bm, name), mat, loc, rot, parent=parent)


def tube(name, loc, pts, radius, mat, parent, col=None):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (*co, 1.0)
    sp.use_endpoint_u = True
    sp.order_u = 3
    sp.resolution_u = 16
    sp.use_smooth = True
    return link_obj(name, cu, mat, loc, parent=parent, col=col)


def joint(name, loc, parent=None, size=0.03):
    e = link_obj(name, None, loc=loc, parent=parent)
    e.empty_display_type = "SPHERE"
    e.empty_display_size = size
    return e


AX_X = (0, R(90), 0)  # cylinder axis along X
AX_Y = (R(90), 0, 0)  # cylinder axis along Y

# ---------------------------------------------------------------- rig (pivot empties)
# Robot faces -Y. Its left side (L) is +X.
root = joint("Alu_root", (0, 0, 0), size=0.12)
body = joint("body", (0, 0, 0.34), root, 0.08)
neck = joint("neck", (0, 0, 0.585), body)
head = joint("head", (0, 0, 0.62), neck, 0.06)
antenna = joint("antenna", (0.29, 0.05, 0.84), head)

arm = {}
leg = {}
for side, sx in (("L", 1), ("R", -1)):
    a1 = joint(f"arm_{side}_1", (0.185 * sx, 0, 0.535), body)
    a2 = joint(f"arm_{side}_2", (0.19 * sx, 0, 0.445), a1)
    a3 = joint(f"arm_{side}_3", (0.19 * sx, 0, 0.30), a2)
    l1 = joint(f"leg_{side}_1", (0.085 * sx, 0, 0.315), body)
    l2 = joint(f"leg_{side}_2", (0.09 * sx, 0, 0.215), l1)
    l3 = joint(f"leg_{side}_3", (0.09 * sx, 0, 0.07), l2)
    arm[side] = (a1, a2, a3)
    leg[side] = (l1, l2, l3)

# ---------------------------------------------------------------- head
head_shell = rbox("Head_Shell", (0, 0, 0.80), (0.50, 0.40, 0.36), 0.065, M["shell"], head, segs=6)
cutter = rbox("Head_ScreenCutter", (0, -0.20, 0.79), (0.40, 0.07, 0.27), 0.045, None, head, segs=6)
cutter.display_type = "WIRE"
cutter.hide_render = True
boo = head_shell.modifiers.new("ScreenRecess", "BOOLEAN")
boo.operation = "DIFFERENCE"
boo.solver = "EXACT"
boo.object = cutter

rbox("Head_Screen", (0, -0.172, 0.79), (0.385, 0.03, 0.255), 0.04, M["screen"], head, segs=6)
for side, sx in (("L", 1), ("R", -1)):
    sph(f"Eye_{side}", (0.08 * sx, -0.187, 0.80), 1.0, M["eye"], head, scale=(0.032, 0.006, 0.047))
    for zt, zn in ((1, "T"), (-1, "B")):
        cyl(f"Screen_Screw_{side}{zn}", (0.168 * sx, -0.187, 0.79 + 0.1 * zt), 0.011, 0.006,
            M["metal"], head, rot=AX_Y, segs=24, bevel=0.002)

# little "w" cat mouth (Robot_One)
tube("Mouth", (0, -0.188, 0.745),
     [(-0.024, 0, 0.007), (-0.012, 0, -0.008), (0, 0, 0.003), (0.012, 0, -0.008), (0.024, 0, 0.007)],
     0.0032, M["eye"], head)

# ear disks (both refs) - ocean ring, cyan hub ring, metal cap
for side, sx in (("L", 1), ("R", -1)):
    cyl(f"Ear_{side}_Base", (0.256 * sx, 0.03, 0.80), 0.105, 0.03, M["ocean"], head, rot=AX_X, bevel=0.008)
    cyl(f"Ear_{side}_Plate", (0.274 * sx, 0.03, 0.80), 0.078, 0.014, M["metal"], head, rot=AX_X, bevel=0.004)
    torus(f"Ear_{side}_Glow", (0.279 * sx, 0.03, 0.80), 0.083, 0.0055, M["glow"], head, rot=AX_X)
    cyl(f"Ear_{side}_Cap", (0.284 * sx, 0.03, 0.80), 0.042, 0.014, M["shell"], head, rot=AX_X, bevel=0.005)

# antenna from the left ear (Robot_Two)
tube("Antenna_Rod", (0.29, 0.05, 0.84),
     [(0, 0, 0), (0.012, 0.01, 0.10), (0.02, 0.05, 0.22), (0.01, 0.11, 0.31)],
     0.0055, M["metal"], antenna)
sph("Antenna_Tip", (0.30, 0.16, 1.15), 0.019, M["glow"], antenna)
cyl("Antenna_Base", (0.29, 0.05, 0.835), 0.016, 0.03, M["joint"], antenna)

# top slot (Robot_One) and a small rear vent block (Robot_Two)
rbox("Head_TopSlot", (-0.11, -0.11, 0.978), (0.09, 0.035, 0.014), 0.006, M["sky"], head, segs=3)
rbox("Head_TopBlock", (0.06, 0.06, 0.98), (0.08, 0.06, 0.022), 0.009, M["joint"], head, segs=3)

# ---------------------------------------------------------------- neck + torso
cyl("Neck", (0, 0, 0.605), 0.045, 0.05, M["joint"], neck)
torus("Neck_Collar", (0, 0, 0.59), 0.056, 0.011, M["metal"], neck)

rbox("Chest", (0, 0, 0.50), (0.30, 0.22, 0.17), 0.045, M["shell"], body, segs=6, bottom=(0.86, 0.92))
cyl("Chest_Button", (-0.07, -0.108, 0.515), 0.021, 0.014, M["joint"], body, rot=AX_Y, bevel=0.004)
for i, x in enumerate((0.045, 0.065, 0.085)):
    rbox(f"Chest_Light_{i}", (x, -0.111, 0.515), (0.011, 0.008, 0.032), 0.003, M["glow"], body, segs=2)
rbox("Back_Strip", (0, 0.111, 0.52), (0.14, 0.012, 0.022), 0.005, M["glow"], body, segs=2)

cyl("Waist", (0, 0, 0.40), 0.095, 0.07, M["joint"], body, scale=(1, 0.72, 1), bevel=0.012)
torus("Waist_Ring", (0, 0, 0.41), 0.095, 0.007, M["metal"], body).scale = (1, 0.74, 1)
rbox("Pelvis", (0, 0, 0.345), (0.21, 0.15, 0.075), 0.03, M["ocean"], body, segs=5)

# ---------------------------------------------------------------- arms
for side, sx in (("L", 1), ("R", -1)):
    a1, a2, a3 = arm[side]
    sph(f"Shoulder_{side}", (0.185 * sx, 0, 0.535), 0.04, M["joint"], a1)
    rbox(f"Shoulder_{side}_Pad", (0.198 * sx, 0, 0.555), (0.085, 0.105, 0.065), 0.03, M["shell"], a1, segs=5)
    cyl(f"UpperArm_{side}", (0.19 * sx, 0, 0.49), 0.025, 0.09, M["joint"], a1)
    sph(f"Elbow_{side}", (0.19 * sx, 0, 0.445), 0.031, M["joint"], a2)
    cyl(f"Forearm_{side}", (0.19 * sx, 0, 0.375), 0.057, 0.13, M["ocean"], a2, r2=0.04, bevel=0.012)
    cyl(f"Forearm_{side}_Cuff", (0.19 * sx, 0, 0.31), 0.047, 0.012, M["rubber"], a2, bevel=0.003)
    torus(f"Forearm_{side}_Glow", (0.19 * sx, 0, 0.312), 0.052, 0.003, M["glow"], a2)
    sph(f"Palm_{side}", (0.19 * sx, 0, 0.283), 1.0, M["joint"], a3, scale=(0.033, 0.039, 0.031))
    for fy, fn in ((-1, "F"), (1, "B")):
        rbox(f"Finger_{side}{fn}", (0.19 * sx, 0.022 * fy, 0.25), (0.028, 0.017, 0.058), 0.0075,
             M["metal"], a3, segs=3, rot=(R(-14 * fy), 0, 0))

# ---------------------------------------------------------------- legs
for side, sx in (("L", 1), ("R", -1)):
    l1, l2, l3 = leg[side]
    x = 0.09 * sx
    sph(f"Hip_{side}", (0.085 * sx, 0, 0.315), 0.038, M["joint"], l1)
    cyl(f"Thigh_{side}", (x, 0, 0.27), 0.033, 0.09, M["joint"], l1)
    rbox(f"Knee_{side}", (x, -0.012, 0.215), (0.09, 0.10, 0.07), 0.028, M["shell"], l2, segs=5)
    rbox(f"Shin_{side}", (x, 0.0, 0.13), (0.118, 0.13, 0.125), 0.03, M["ocean"], l2, segs=5, top=(0.86, 0.86))
    cyl(f"Ankle_{side}", (x, 0, 0.072), 0.03, 0.03, M["joint"], l3)
    rbox(f"Foot_{side}", (x, -0.025, 0.05), (0.118, 0.17, 0.056), 0.024, M["shell"], l3, segs=5)
    rbox(f"Sole_{side}", (x, -0.025, 0.013), (0.106, 0.158, 0.026), 0.01, M["rubber"], l3, segs=3)
    # heel wheel (Robot_One)
    wx = 0.158 * sx
    w = cyl(f"wheel_{side}", (wx, 0.05, 0.032), 0.032, 0.026, M["rubber"], l3, rot=AX_X, bevel=0.008)
    torus(f"wheel_{side}_Hub", (wx + 0.013 * sx, 0.05, 0.032), 0.017, 0.0035, M["glow"], l3, rot=AX_X)
    cyl(f"wheel_{side}_Cap", (wx + 0.013 * sx, 0.05, 0.032), 0.011, 0.006, M["metal"], l3, rot=AX_X, bevel=0.002)

# ---------------------------------------------------------------- parenting
bpy.context.view_layer.update()
for child, par in PARENT:
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()
try:
    cutter.hide_set(True)
except Exception:
    pass

# ---------------------------------------------------------------- pose
head.rotation_euler = (R(-4), R(7), R(14))      # curious tilt toward camera
antenna.rotation_euler = (R(-6), 0, 0)
for side, sx in (("L", 1), ("R", -1)):
    a1, a2, a3 = arm[side]
    a1.rotation_euler = (R(4), R(-11 * sx), 0)  # slight A-pose
    a2.rotation_euler = (R(-22), 0, 0)          # elbows bend forward
arm["L"][2].rotation_euler = (0, 0, R(20))
# wave with the right arm - it swings into open space on the frame's left
arm["R"][0].rotation_euler = (R(-25), R(100), 0)
arm["R"][1].rotation_euler = (0, R(48), 0)
arm["R"][2].rotation_euler = (0, R(10), R(-30))

# ---------------------------------------------------------------- stage
def cyclorama(name, mat, width=12.0, front=-5.0, start=1.0, radius=1.4, height=6.0, segs=20):
    prof = [(front, 0.0), (start, 0.0)]
    for i in range(1, segs + 1):
        a = -math.pi / 2 + (math.pi / 2) * i / segs
        prof.append((start + radius * math.cos(a), radius + radius * math.sin(a)))
    prof.append((start + radius, height))
    bm = bmesh.new()
    left = [bm.verts.new((-width / 2, y, z)) for y, z in prof]
    right = [bm.verts.new((width / 2, y, z)) for y, z in prof]
    for i in range(len(prof) - 1):
        bm.faces.new((left[i], right[i], right[i + 1], left[i + 1]))
    return link_obj(name, finish_mesh(bm, name), mat, col=STAGE)


backdrop_mat = make_mat("Alu_Backdrop", "#B4CEDD", rough=0.9)
cyclorama("Backdrop", backdrop_mat)


def area_light(name, loc, target, power, size, color="#FFFFFF"):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.shape = "DISK"
    ld.size = size
    ld.color = lin(color)[:3]
    o = link_obj(name, ld, loc=loc, col=STAGE)
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


area_light("Key", (-2.0, -1.0, 2.3), (0, 0, 0.45), 300, 0.5, "#FFF4E8")
area_light("Top", (0.15, -0.25, 2.7), (0, 0, 0), 30, 2.0, "#FFFFFF")
area_light("Fill", (2.2, -1.4, 1.0), (0, 0, 0.5), 14, 2.0, "#E4F3FA")
area_light("Rim", (0.9, 1.6, 2.0), (0, 0, 0.75), 140, 0.8, "#DDF4FF")

cd = bpy.data.cameras.new("Alu_Cam")
cd.lens = 72
cam = link_obj("Alu_Cam", cd, loc=(1.25, -2.55, 0.92), col=STAGE)
cam.rotation_euler = (Vector((0.02, 0, 0.57)) - cam.location).to_track_quat("-Z", "Y").to_euler()
cd.dof.use_dof = True
cd.dof.focus_object = head
cd.dof.aperture_fstop = 4.0
SC.camera = cam

# world
w = bpy.data.worlds.get("Alu_World") or bpy.data.worlds.new("Alu_World")
if w.node_tree is None:
    try:
        w.use_nodes = True
    except Exception:
        pass
if w.node_tree is not None:
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = lin("#C4DCEA")
    bg.inputs[1].default_value = 0.16
w.color = lin("#D3E8F3")[:3]
SC.world = w

# render settings
SC.render.engine = "BLENDER_EEVEE"
SC.render.resolution_x = 1200
SC.render.resolution_y = 1500
SC.render.resolution_percentage = 100
SC.eevee.taa_render_samples = 128
for attr, val in (("use_raytracing", True), ("use_shadows", True), ("shadow_ray_count", 3), ("shadow_step_count", 12)):
    try:
        setattr(SC.eevee, attr, val)
    except Exception:
        pass

SC.render.engine = "CYCLES"
SC.cycles.device = "CPU"
SC.cycles.samples = 160
SC.cycles.use_adaptive_sampling = True
SC.cycles.use_denoising = True

# hide (not delete) the default startup objects
for n in ("Cube", "Light"):
    o = bpy.data.objects.get(n)
    if o:
        o.hide_render = True
        try:
            o.hide_set(True)
        except Exception:
            pass

# colour management + glow on the emissives
vs = SC.view_settings
vs.view_transform = "AgX"
vs.exposure = -0.2
for look in ("AgX - Medium High Contrast", "AgX - Base Contrast"):
    try:
        vs.look = look
        break
    except Exception:
        pass

ng = bpy.data.node_groups.get("Alu_Comp") or bpy.data.node_groups.new("Alu_Comp", "CompositorNodeTree")
ng.nodes.clear()
for item in list(ng.interface.items_tree):
    ng.interface.remove(item)
ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
rl = ng.nodes.new("CompositorNodeRLayers")
gl = ng.nodes.new("CompositorNodeGlare")
gout = ng.nodes.new("NodeGroupOutput")
rl.location, gl.location, gout.location = (-400, 0), (-100, 0), (200, 0)
for v in ("Bloom", "BLOOM"):
    try:
        gl.inputs["Type"].default_value = v
        break
    except Exception:
        pass
gl.inputs["Threshold"].default_value = 2.0
gl.inputs["Strength"].default_value = 0.3
gl.inputs["Size"].default_value = 0.45
ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
ng.links.new(gl.outputs[0], gout.inputs[0])
SC.compositing_node_group = ng
SC.render.use_compositing = True

result = {"glare_type": gl.inputs["Type"].default_value, "objects": len(COL.all_objects), "stage": len(STAGE.all_objects)}
