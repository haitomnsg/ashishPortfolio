# Builds the hero ("Arrival") world for the portfolio, matched to the approved key art
# inspo/Section_One.png: a low camera on a limestone terrace at the cliff edge, the glass gate,
# Alu beside it, pines, boulders, grass, a red-earth path, the sea and a far headland.
#
# How the look is matched (see docs/world/README.md):
#   - Hero_Cam reproduces the key art's camera: 34 mm, level, lens-shifted so the horizon sits
#     at row 620 of 1024. Every prop below is placed by back-projecting where it is in the key
#     art (img_ground / img_depth), so it lands on the same pixels.
#   - The far world (sky, cloud, headland, sea) is a matte painting made from the key art by
#     docs/world/backdrop_build.py and drawn on the web as a dome at infinity.
#   - The near world is a set of proxy meshes (material "Proj") that the web paints by
#     projecting public/images/hero/plate.webp from the hero camera, so at rest the screen is
#     the key art, and when the camera moves the geometry gives true parallax.
#   - Alu, the gate glass and light, and the grass tufts are real 3D, lit and animated.
#
# Idempotent: rerunning removes and rebuilds the "Hero_World" collection. Alu is appended
# from docs/robot/alu_v2.blend (waving pose) into "Alu" if missing. Blender 5.1.
# Coordinates: metres, Z up, the visitor (camera) at -Y looking toward +Y, the gate's base
# centre at the origin's x/y. Ground in front of the step is z = 0.
#
# Run headless:  blender --background --factory-startup --python docs/world/hero_build.py
# (writes hero.blend, public/models/world/hero.glb and renders/coverage.png).
import bpy, bmesh, math, random, os, sys
from mathutils import Vector, noise

R = math.radians
SC = bpy.context.scene
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) \
    if "__file__" in dir() else r"D:\AshishPortfolio"
if not os.path.isdir(os.path.join(ROOT, "docs")):
    ROOT = r"D:\AshishPortfolio"

# ---------------------------------------------------------------- the key art's camera
IMG_W, IMG_H = 1536, 1024
F = 34 / 36 * IMG_W            # focal length in pixels (34 mm lens, 36 mm sensor)
CX, HY = 768.0, 620.0          # image centre column, horizon row
Z_SLAB = 0.181                 # terrace top (where the gate and Alu stand)
Z_STEP = 0.110
EYE = 0.6574                   # camera height above the terrace (from Alu's 303 px height)
CAM = Vector((0.0, -7.170, Z_SLAB + EYE))


def ray(u, v):
    return Vector(((u - CX) / F, 1.0, (HY - v) / F))


def img_ground(u, v, z):
    """The point on the horizontal plane z that the key art pixel (u, v) shows."""
    d = ray(u, v)
    t = (z - CAM.z) / d.z
    return CAM + d * t


def img_depth(u, v, t):
    """The point at forward distance t (metres from the camera) behind pixel (u, v)."""
    return CAM + ray(u, v) * t


def depth_at(v, z):
    return F * (CAM.z - z) / (v - HY)


def px(n, t):
    """n pixels of the key art, in metres, at forward distance t."""
    return n * t / F


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


purge_collection("Hero_World")
for n in ("Cube", "Light", "Camera"):      # default-scene leftovers
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
    for d in list(coll):
        if d.users == 0:
            coll.remove(d)


def new_col(name, parent=None):
    col = bpy.data.collections.new(name)
    (parent or SC.collection).children.link(col)
    return col


WORLD = new_col("Hero_World")
C_GROUND = new_col("Ground", WORLD)
C_GATE = new_col("Gate", WORLD)
C_PROPS = new_col("Props", WORLD)
C_RIG = new_col("Rig", WORLD)          # camera, lights


# ---------------------------------------------------------------- colour + materials
def lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


# authored colours, sampled from the key art (sRGB)
PAL = {
    "gold":       "#F4B23C",   # dry golden tufts, sunlit tips
    "gold_mid":   "#E58A2E",
    "gold_base":  "#9A5A22",
    "green":      "#7E9440",   # spiky green tufts
    "green_base": "#3F4A24",
    "frame":      "#F3E6DC",   # gate frame (only seen if the projection is missing)
}


def make_mat(name, hexc, rough=0.9, spec=0.25, vcol=False, emit=None, strength=0.0,
             alpha=1.0, transmission=0.0):
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
    if alpha < 1.0:
        I["Alpha"].default_value = alpha
        for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
            try:
                setattr(m, attr, val)
            except Exception:
                pass
    if transmission > 0:
        I["Transmission Weight"].default_value = transmission
        I["IOR"].default_value = 1.45
    m.use_backface_culling = False
    m.diffuse_color = lin(emit or hexc)
    return m


M = {
    # painted by projection on the web; the vertex colours are the plate sampled per vertex
    # (what the web shows where the projection has nothing better)
    "proj":  make_mat("Proj", "#FFFFFF", rough=1.0, spec=0.0, vcol=True),
    "paint": make_mat("World_Paint", "#FFFFFF", rough=0.92, spec=0.22, vcol=True),
    "glass": make_mat("Gate_Glass", "#DDF4FF", rough=0.05, spec=0.6, alpha=0.16, transmission=0.9),
    "light": make_mat("Gate_Light", "#FFF4D6", rough=1.0, spec=0.0, emit="#FFF1C9", strength=1.4, alpha=0.10),
}


# ---------------------------------------------------------------- geometry helpers
def link_obj(name, data, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), col=None, parent=None):
    o = bpy.data.objects.new(name, data)
    (col or C_PROPS).objects.link(o)
    o.location, o.rotation_euler, o.scale = loc, rot, scale
    if mat is not None and data is not None:
        data.materials.append(mat)
    if parent is not None:
        o.parent = parent
    return o


def flat_mesh(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False
    return me


def ensure_col_attr(me):
    attr = me.color_attributes.get("Col")
    if attr is None:
        attr = me.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    me.color_attributes.active_color = attr
    return attr


def add_bevel(o, width, segs=1):
    md = o.modifiers.new("Bevel", "BEVEL")
    md.width, md.segments = width, segs
    md.limit_method = "ANGLE"
    md.angle_limit = R(40)
    md.harden_normals = False
    return md


def hash_noise(x, y, scale=1.0, seed=0):
    return noise.noise(Vector((x * scale + seed * 13.1, y * scale + seed * 7.7, seed * 3.3)))


def prism(name, pts_xy, z_top, z_bot, col=None, mat="proj", bevel=0.0, subdiv=0):
    """A flat-topped block from a polygon outline (world XY), top at z_top, sides down to z_bot."""
    bm = bmesh.new()
    vs = [bm.verts.new((p[0], p[1], z_bot)) for p in pts_xy]
    f = bm.faces.new(vs)
    if f.normal.z > 0:
        f.normal_flip()
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    top = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    for v in top:
        v.co.z = z_top
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    if subdiv:
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
    o = link_obj(name, flat_mesh(bm, name), M[mat], col=col or C_GROUND)
    if bevel:
        add_bevel(o, bevel, 1)
    return o


def ground_poly(name, img_pts, z, z_bot, **kw):
    """prism() with the top outline given as key-art pixels on the plane z."""
    pts = [img_ground(u, v, z) for (u, v) in img_pts]
    return prism(name, [(p.x, p.y) for p in pts], z, z_bot, **kw)


# ---------------------------------------------------------------- the terrace, ground and step
def terrace():
    """The ground plane in front, the limestone terrace at the cliff edge (its back edge is the
    key art's sea line), the wide step, and the taller blocks on the right."""
    # ground (z = 0): a grid from just in front of the camera to under the terrace
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=60, y_segments=36, size=1.0)
    for v in bm.verts:
        x, y = v.co.x * 9.0, CAM.y + 1.2 + (v.co.y + 1) * 0.5 * 6.6     # to 7.8 m: under the terrace
        v.co = Vector((x, y, 0.0))
    o = link_obj("Ground", flat_mesh(bm, "Ground"), M["proj"], col=C_GROUND)

    # the terrace: back edge follows the sea line (pixels), front edge as painted
    back = [(-260, 700), (120, 700), (205, 706), (290, 712), (330, 714), (400, 716), (440, 721),
            (500, 727), (560, 731), (620, 734), (640, 742), (700, 744), (900, 738), (930, 732),
            (1000, 735), (1060, 740), (1110, 743), (1136, 748), (1150, 765), (1168, 784),
            (1186, 784), (1200, 776), (1260, 772), (1300, 767), (1330, 757), (1350, 745),
            (1376, 744), (1536, 744), (1820, 744)]
    front = [(1820, 800), (1536, 798), (1330, 796), (1190, 800), (1150, 790), (1010, 787),
             (640, 787), (520, 794), (440, 790), (360, 776), (300, 766), (250, 735), (120, 728),
             (-260, 728)]
    ground_poly("Terrace", back + front, Z_SLAB, -0.4)

    # far left, behind the rock and the pine: higher ground stepping back from the cliff
    t0 = 13.0
    zt = CAM.z - px(640 - HY, t0)
    # its right edge runs along the camera ray through column 212, so it never fans out
    prism("Mound_FarL", [(px(-300 - CX, t0), CAM.y + t0), (px(212 - CX, t0), CAM.y + t0),
                         (px(212 - CX, t0 + 4), CAM.y + t0 + 4), (px(-300 - CX, t0 + 4), CAM.y + t0 + 4)], zt, -0.4)

    # the step below the gate
    ground_poly("Step", [(612, 818), (994, 815), (994, 797), (612, 797)], Z_STEP, -0.2, bevel=0.012)

    # big block right of the step (taller than the terrace): top front edge at 760, face to 840
    t_f = depth_at(840, 0.0)
    z_top = CAM.z - (760 - HY) * t_f / F
    blk = [(1000, 744), (1112, 739), (1160, 748), (1158, 761), (1040, 766), (1000, 760)]
    ground_poly("Block_R", blk, z_top, -0.2, bevel=0.015)

    # the slab the right pine stands on, and its neighbour
    ground_poly("Slab_R2", [(1186, 786), (1330, 778), (1340, 800), (1330, 812), (1190, 815)], Z_SLAB + 0.02, -0.3, bevel=0.012)
    ground_poly("Slab_R3", [(1330, 772), (1536, 766), (1820, 766), (1820, 792), (1536, 790), (1340, 788)], Z_SLAB + 0.07, -0.3, bevel=0.012)
    # the slab cluster left of Alu
    ground_poly("Slab_L", [(300, 718), (470, 726), (520, 790), (440, 792), (360, 778), (300, 764)], Z_SLAB + 0.02, -0.3, bevel=0.012)
    # stepping stones beside the path (thin, just proud of the ground)
    for i, pts in enumerate([
        [(430, 842), (640, 838), (700, 866), (480, 872)],
        [(640, 860), (840, 858), (830, 886), (650, 888)],
        [(880, 838), (1060, 836), (1040, 868), (900, 870)],
        [(150, 904), (560, 900), (600, 990), (180, 1000)],
        [(-60, 980), (600, 990), (640, 1100), (-60, 1100)],
        [(940, 966), (1250, 960), (1300, 1100), (900, 1100)],
    ]):
        ground_poly("Flag_%02d" % i, pts, 0.035, -0.1, bevel=0.01)
    return o


# ---------------------------------------------------------------- rocks
def rock(name, u0, u1, v_top, v_base, z_base, depth_k=0.8, seed=0, flat_top=0.0):
    """A boulder whose silhouette spans key-art columns u0..u1 and rows v_top..v_base."""
    rr = random.Random(seed)
    c = img_ground((u0 + u1) / 2, v_base, z_base)
    t = c.y - CAM.y
    w = px(u1 - u0, t)
    h = px(v_base - v_top, t) * 1.04
    d = w * depth_k
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    for v in bm.verts:
        v.co.x *= 0.5 * w * rr.uniform(0.96, 1.05)
        v.co.y *= 0.5 * d * rr.uniform(0.9, 1.1)
        z = v.co.z
        v.co.z = (z + 1.0) * 0.5 * h if z > -0.2 else (z + 1.0) * 0.5 * h * 0.3
        if flat_top and v.co.z > h * (1 - flat_top):
            v.co.z = h * (1 - flat_top) + (v.co.z - h * (1 - flat_top)) * 0.35
    loc = Vector((c.x, c.y + d * 0.42, z_base - 0.04))
    return link_obj(name, flat_mesh(bm, name), M["proj"], loc)


# ---------------------------------------------------------------- pines (proxy silhouettes)
def pine(name, u_axis, v_base, z_base, seed=0, trunk=(20, 13)):
    """A pine whose silhouette matches the key art. The rows come from renders/pines.json
    (written by backdrop_build.py): (row, left column, right column) from the top down. Each
    row becomes a ring centred on that row's span, so the faceted proxy covers the painted
    tree on both sides. Sways on the web (the projection uses the rest pose)."""
    import json
    with open(os.path.join(ROOT, "docs", "world", "renders", "pines.json")) as fh:
        rows = json.load(fh)[name]
    base = img_ground(u_axis, v_base, z_base)
    t = base.y - CAM.y
    rr = random.Random(seed)
    bm = bmesh.new()
    seg = 10
    rings = []
    for (row, L, Rr) in rows[1:]:
        z = px(v_base - row, t)
        cx = px((L + Rr) / 2 - u_axis, t)
        r = max(0.02, px((Rr - L) / 2 + 6, t))
        ring = []
        for i in range(seg):
            a = i / seg * math.tau
            ring.append(bm.verts.new((cx + math.cos(a) * r, math.sin(a) * r * 0.8, z)))
        rings.append(ring)
    r0, L0, R0 = rows[0]
    tip = bm.verts.new((px((L0 + R0) / 2 - u_axis, t), 0, px(v_base - r0 + 4, t)))
    for i in range(seg):
        bm.faces.new((rings[0][i], rings[0][(i + 1) % seg], tip))
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            bm.faces.new((a[i], a[(i + 1) % seg], b[(i + 1) % seg], b[i]))
    bm.faces.new(list(reversed(rings[-1])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    fol = link_obj(name, flat_mesh(bm, name), M["proj"], (base.x, base.y, z_base))
    bm = bmesh.new()
    th = px(v_base - rows[-1][0], t) + 0.1
    bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=px(trunk[0], t),
                          radius2=px(trunk[1], t), depth=th)
    for v in bm.verts:
        v.co.z += th / 2 - 0.05
    tr = link_obj(name + "_Trunk", flat_mesh(bm, name + "_Trunk"), M["proj"], (base.x, base.y, z_base))
    return fol, tr


# ---------------------------------------------------------------- tufts (real 3D, animated)
# the key art's light for baked tuft paint: high, from the upper left and a little in front
TUFT_LIGHT = Vector((-0.55, -0.45, 0.70)).normalized()
TUFT_PAL = {
    "gold":  ("#A0561A", "#DE8A22", "#FBB733", "#FFD257"),   # base, shade, lit, lit tip
    "green": ("#26391A", "#3E5A26", "#64843A", "#7A9842"),
}


def tuft(name, loc, h, reach, seed, blades=12, kind="gold", lean=(20, 64), width=0.22):
    """Agave-like tuft as painted: wide pointed blades folded along a midrib, fanning out
    from one point. Paint is baked per face (sunlit side vs shade, darker at the base) and
    shown unlit on the web; a vertex's height above the base is its bend weight there."""
    rr = random.Random(seed)
    bm = bmesh.new()
    base = Vector((0, 0, 0))
    for i in range(blades):
        az = i / blades * math.tau + rr.uniform(-0.25, 0.25)
        ln = R(rr.uniform(*lean))
        L = h / math.cos(ln) * rr.uniform(0.72, 1.0)
        L = min(L, reach / max(0.2, math.sin(ln)))
        d = Vector((math.cos(az) * math.sin(ln), math.sin(az) * math.sin(ln), math.cos(ln)))
        side = Vector((-math.sin(az), math.cos(az), 0))
        n = side.cross(d).normalized()
        w = width * L * rr.uniform(0.85, 1.15)
        tip = base + d * L + Vector((0, 0, -0.06 * L * math.sin(ln)))
        root = base + d * 0.01
        mid = root + d * (0.28 * L)
        bl = root + side * (w / 2) - n * (w * 0.22)
        br = root - side * (w / 2) - n * (w * 0.22)
        ml = mid + side * (w * 0.42) - n * (w * 0.18)
        mr = mid - side * (w * 0.42) - n * (w * 0.18)
        vb, vl, vr, vml, vmr, vm, vt = (bm.verts.new(p) for p in (root, bl, br, ml, mr, mid + n * 0.004, tip))
        for f in ((vl, vb, vm, vml), (vb, vr, vmr, vm), (vml, vm, vt), (vm, vmr, vt)):
            bm.faces.new(f)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = flat_mesh(bm, name)
    rot = rr.uniform(0, 6.28)
    o = link_obj(name, me, M["paint"], loc, (0, 0, rot))
    attr = ensure_col_attr(me)
    c_base, c_shade, c_lit, c_tip = (Vector(lin(x)[:3]) for x in TUFT_PAL[kind])
    rz = o.rotation_euler.to_matrix()
    for p in me.polygons:
        nn = rz @ p.normal
        lit = max(0.0, nn.dot(TUFT_LIGHT)) if nn.z > -0.2 else 0.0
        lit = min(1.0, lit * 1.5)
        k = 0.92 + 0.16 * rr.random()
        for li in p.loop_indices:
            vz = me.vertices[me.loops[li].vertex_index].co.z
            tt = min(1.0, max(0.0, vz / max(h, 0.01)))
            face = c_shade.lerp(c_lit, lit)
            top = c_lit.lerp(c_tip, lit)
            c = (c_base.lerp(face, min(1.0, tt * 2.2)) if tt < 0.45 else face.lerp(top, (tt - 0.45) / 0.55)) * k
            attr.data[li].color = (c.x, c.y, c.z, 1.0)
    return o


# ---------------------------------------------------------------- gate
def rounded_rect(w, h, r, n=6, z0=0.0):
    """Points of a rounded rectangle in XZ, centred at x=0, from z=z0 to z=z0+h."""
    pts = []
    cx, cz = w / 2 - r, z0 + h - r
    corners = [(cx, cz, 0), (-cx, cz, 90), (-cx, z0 + r, 180), (cx, z0 + r, 270)]
    for (px_, pz, a0) in corners:
        for i in range(n + 1):
            a = R(a0 + 90 * i / n)
            pts.append(Vector((px_ + math.cos(a) * r, 0.0, pz + math.sin(a) * r)))
    return pts


def gate():
    """The glass gate, measured off the key art: outer 254 x 506 px, opening 214 x 466 px,
    corner radii 26 / 22 px, flared feet. It stands at the origin on the terrace."""
    t = -CAM.y
    k = t / F
    W, H = 260 * k, 508 * k                  # 254 x 506 px painted, +3 / +2 px all round
    WI, HI = 214 * k, 466 * k                # opening
    zi = 21 * k                              # the bottom bar
    D = 0.12
    gx = px(770 - CX, t)                     # centre column 770
    outer = rounded_rect(W, H, 28 * k, 7, -2 * k)
    inner = rounded_rect(WI, HI, 22 * k, 7, zi)
    bm = bmesh.new()
    vo = [bm.verts.new(p + Vector((0, -D / 2, 0))) for p in outer]
    vi = [bm.verts.new(p + Vector((0, -D / 2, 0))) for p in inner]
    n = len(vo)
    faces = [bm.faces.new((vo[i], vo[(i + 1) % n], vi[(i + 1) % n], vi[i])) for i in range(n)]
    res = bmesh.ops.extrude_face_region(bm, geom=faces)
    ev = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ev, vec=(0, D, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    frame = link_obj("Gate_Frame", flat_mesh(bm, "Gate_Frame"), M["proj"], (gx, 0, Z_SLAB), col=C_GATE)
    add_bevel(frame, 0.01, 2)
    # flared feet (the painted frame widens 7 px each side over its last 17 px)
    for sx, nm in ((-1, "Gate_Foot_L"), (1, "Gate_Foot_R")):
        x_out, x_in = sx * (W / 2 + 7 * k), sx * (W / 2 - 22 * k)
        bm = bmesh.new()
        prof = [(x_out, 0), (x_in, 0), (x_in, 17 * k), (sx * W / 2, 17 * k)]
        vf = [bm.verts.new((p[0], -D / 2 - 0.012, p[1])) for p in prof]
        f = bm.faces.new(vf)
        res = bmesh.ops.extrude_face_region(bm, geom=[f])
        bmesh.ops.translate(bm, verts=[e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)],
                            vec=(0, D + 0.024, 0))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        link_obj(nm, flat_mesh(bm, nm), M["proj"], (gx, 0, Z_SLAB), col=C_GATE)

    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in rounded_rect(WI, HI, 22 * k, 7, zi)]
    bm.faces.new(vs)
    glass = link_obj("Gate_Glass", flat_mesh(bm, "Gate_Glass"), M["glass"], (gx, 0.0, Z_SLAB), col=C_GATE)
    for p in glass.data.polygons:
        p.use_smooth = True
    # UVs for the glass shader: u across, v up
    uvl = glass.data.uv_layers.new(name="UVMap")
    for loop in glass.data.loops:
        co = glass.data.vertices[loop.vertex_index].co
        uvl.data[loop.index].uv = ((co.x + WI / 2) / WI, (co.z - zi) / HI)

    # light spilling from the opening onto the terrace (toward the visitor) and a haze card
    bm = bmesh.new()
    a = [bm.verts.new(Vector(p)) for p in ((-WI / 2, -0.06, 0.004), (WI / 2, -0.06, 0.004),
                                              (WI / 2 + 0.9, -2.4, 0.004), (-WI / 2 - 0.9, -2.4, 0.004))]
    bm.faces.new(a)
    link_obj("Gate_LightShaft", flat_mesh(bm, "Gate_LightShaft"), M["light"], (gx, 0, Z_SLAB), col=C_GATE)
    bm = bmesh.new()
    b = [bm.verts.new(Vector(p)) for p in ((-WI / 2, 0.02, zi), (WI / 2, 0.02, zi),
                                              (WI / 2, 0.02, zi + HI), (-WI / 2, 0.02, zi + HI))]
    bm.faces.new(b)
    link_obj("Gate_Haze", flat_mesh(bm, "Gate_Haze"), M["light"], (gx, 0, Z_SLAB), col=C_GATE)
    return frame, glass


# ---------------------------------------------------------------- build the scene
terrace()
gate()

rock("Rock_L", -10, 302, 660, 782, 0.0, depth_k=0.75, seed=51, flat_top=0.25)
rock("Rock_BL", -40, 226, 842, 960, 0.0, depth_k=0.7, seed=52, flat_top=0.35)
rock("Rock_BR", 1212, 1600, 826, 996, 0.0, depth_k=0.75, seed=53, flat_top=0.15)
rock("Rock_S", 336, 392, 812, 834, 0.0, depth_k=0.8, seed=54, flat_top=0.4)

# pines: (row, half-width px) from the top down, read off the key art's silhouettes
pine("Pine_L", 80, 700, Z_SLAB, seed=41)
pine("Pine_R", 1494, 772, Z_SLAB + 0.07, seed=42, trunk=(16, 11))

# gold tufts where the key art has them:
# (centre column, base row, height px, width px, surface z) measured off the painted tufts
GOLD = [(246, 772, 64, 86, 0.10), (322, 766, 86, 76, Z_SLAB + 0.02), (420, 895, 76, 112, 0.0),
        (266, 968, 80, 106, 0.0), (612, 748, 70, 66, Z_SLAB), (1090, 874, 88, 132, 0.0),
        (1262, 1004, 84, 86, 0.0)]
for i, (u, v, hpx, wpx, z) in enumerate(GOLD):
    p = img_ground(u, v, z)
    t = p.y - CAM.y
    tuft("Tuft_Gold_%02d" % i, (p.x, p.y, z), px(hpx, t), px(wpx * 0.5, t), 60 + i, blades=10,
         lean=(10, 54), width=0.32)
GREEN = [(198, 1004, 50, 50, 0.0), (520, 866, 30, 36, 0.0), (612, 870, 34, 40, 0.0), (946, 926, 30, 40, 0.0),
         (1178, 976, 40, 50, 0.0), (1400, 1020, 64, 70, 0.0), (1470, 1020, 70, 80, 0.0), (1316, 832, 26, 34, 0.0),
         (560, 1010, 46, 50, 0.0), (1530, 1010, 60, 70, 0.0)]
for i, (u, v, hpx, wpx, z) in enumerate(GREEN):
    p = img_ground(u, v, z)
    t = p.y - CAM.y
    tuft("Tuft_Green_%02d" % i, (p.x, p.y, z), px(hpx, t), px(wpx * 0.5, t), 80 + i, blades=9,
         kind="green", lean=(8, 40), width=0.16)


# ---------------------------------------------------------------- Alu
ALU = {"u": 562, "v": 768, "yaw": 20}


def place_alu():
    col = bpy.data.collections.get("Alu")
    if col is None:
        path = os.path.join(ROOT, "docs", "robot", "alu_v2.blend")
        if os.path.exists(path):
            with bpy.data.libraries.load(path, link=False) as (src, dst):
                dst.collections = [c for c in src.collections if c == "Alu"]
            for c in dst.collections:
                SC.collection.children.link(c)
    root = bpy.data.objects.get("Alu_root")
    if root:
        p = img_ground(ALU["u"], ALU["v"], Z_SLAB)
        root.location = (p.x, p.y, Z_SLAB)
        root.rotation_euler = (0, 0, R(ALU["yaw"]))
    return root


place_alu()
purge_collection("Alu_Stage")


# ---------------------------------------------------------------- per-vertex plate colours
def sample_plate():
    """Vertex colours for every projected mesh: the plate at the vertex's key-art pixel.
    The web uses them only where projecting the plate would be wrong (surfaces the hero
    camera cannot see), so hidden vertices take the colour of the nearest visible one."""
    path = os.path.join(ROOT, "public", "images", "hero", "plate.webp")
    if not os.path.exists(path):
        return
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    pix = list(img.pixels)  # RGBA float, rows bottom-up, linear
    bpy.data.images.remove(img)
    # only the projected meshes block the view for this test
    others = [o for o in SC.objects if o.type == "MESH" and not (o.data.materials and o.data.materials[0].name == "Proj")]
    for o in others:
        o.hide_viewport = True
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()

    def at(u, v):
        x = min(w - 1, max(0, int(u)))
        y = min(h - 1, max(0, int(h - 1 - v)))
        i = (y * w + x) * 4
        return pix[i], pix[i + 1], pix[i + 2]

    for o in WORLD.all_objects:
        if o.type != "MESH" or not o.data.materials or o.data.materials[0].name != "Proj":
            continue
        me = o.data
        attr = ensure_col_attr(me)
        mw = o.matrix_world
        vis = {}
        for vtx in me.vertices:
            wp = mw @ vtx.co
            d = wp - CAM
            if d.y <= 0.05:
                continue
            u, v = CX + F * d.x / d.y, HY - F * d.z / d.y
            hit, loc, *_ = SC.ray_cast(dg, CAM, d.normalized(), distance=d.length + 0.5)
            if hit and (loc - wp).length < 0.06 + d.length * 0.004 and -50 < u < w + 50 and -50 < v < h + 50:
                vis[vtx.index] = at(u, v)
        # spread visible colours to hidden vertices along edges
        cols = dict(vis)
        nbr = {i: [] for i in range(len(me.vertices))}
        for e in me.edges:
            a, b = e.vertices
            nbr[a].append(b)
            nbr[b].append(a)
        for _ in range(60):
            grew = {}
            for i in range(len(me.vertices)):
                if i in cols:
                    continue
                ks = [cols[j] for j in nbr[i] if j in cols]
                if ks:
                    grew[i] = tuple(sum(c[k] for c in ks) / len(ks) for k in range(3))
            if not grew:
                break
            cols.update(grew)
        for li, loop in enumerate(me.loops):
            c = cols.get(loop.vertex_index, (0.8, 0.75, 0.68))
            attr.data[li].color = (c[0], c[1], c[2], 1.0)
    for o in others:
        o.hide_viewport = False
    bpy.context.view_layer.update()


# ---------------------------------------------------------------- light, world, camera, render
sun_d = bpy.data.lights.new("Sun", "SUN")
sun_d.energy = 4.2
sun_d.angle = R(6)
sun_d.color = lin("#FFE3BC")[:3]
sun = link_obj("Sun", sun_d, col=C_RIG)
# the key art's sun: high, upper left, a little behind the scene (backlit fronts)
sun.rotation_euler = (Vector((0, 0, 0)) - Vector((-5.0, 4.0, 7.0))).to_track_quat("-Z", "Y").to_euler()

w = bpy.data.worlds.get("Hero_Sky") or bpy.data.worlds.new("Hero_Sky")
if w.node_tree is None:
    try:
        w.use_nodes = True
    except Exception:
        pass
nt = w.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld")
bg = nt.nodes.new("ShaderNodeBackground")
bg.inputs[0].default_value = lin("#8CC6EE")
bg.inputs[1].default_value = 0.8
nt.links.new(bg.outputs[0], out.inputs[0])
SC.world = w

cd = bpy.data.cameras.new("Hero_Cam")
cd.lens = 34
cd.sensor_width = 36
cd.sensor_fit = "HORIZONTAL"
cd.shift_y = (HY - IMG_H / 2) / IMG_W
cd.clip_start = 0.05
cd.clip_end = 1000
cam = link_obj("Hero_Cam", cd, loc=CAM, col=C_RIG)
cam.rotation_euler = (R(90), 0, 0)
SC.camera = cam

SC.render.resolution_x = IMG_W
SC.render.resolution_y = IMG_H
SC.render.resolution_percentage = 100
bpy.context.view_layer.update()
sample_plate()


# ---------------------------------------------------------------- coverage check
def coverage(path=None):
    """Renders the projected meshes' silhouette from the hero camera (white on transparent)
    to renders/coverage.png, for comparing against the key art's foreground mask."""
    path = path or os.path.join(ROOT, "docs", "world", "renders", "coverage.png")
    hidden = []
    for o in SC.objects:
        keep = o.type == "MESH" and o.name in WORLD.all_objects and o.data.materials \
            and o.data.materials[0].name == "Proj"
        if o.type == "MESH" and not keep and not o.hide_render:
            o.hide_render = True
            hidden.append(o)
    eng = SC.render.engine
    SC.render.engine = "BLENDER_WORKBENCH"
    sh = SC.display.shading
    sh.light, sh.color_type, sh.single_color = "FLAT", "SINGLE", (1, 1, 1)
    SC.render.film_transparent = True
    SC.display.render_aa = "OFF"
    SC.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for o in hidden:
        o.hide_render = False
    SC.render.engine = eng
    SC.render.film_transparent = False
    return path


def export_world(path=None):
    """Writes every Hero_World mesh (not Alu, not the rig) to one GLB with vertex colours."""
    path = path or os.path.join(ROOT, "public", "models", "world", "hero.glb")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    meshes = [o for o in WORLD.all_objects if o.type == "MESH"]
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    kw = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
              export_yup=True, export_normals=True, export_materials="EXPORT",
              export_animations=False, export_lights=False, export_cameras=False,
              export_vertex_color="ACTIVE", export_active_vertex_color_when_no_material=True)
    while True:
        try:
            bpy.ops.export_scene.gltf(**kw)
            break
        except TypeError as e:  # drop unknown keywords on other exporter versions
            bad = str(e).split('"')[1] if '"' in str(e) else None
            if bad and bad in kw:
                kw.pop(bad)
            else:
                raise
    return path


SC.render.engine = "BLENDER_EEVEE"
vs = SC.view_settings
vs.view_transform = "Standard"
vs.look = "None"

if bpy.app.background:
    coverage()
    export_world()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "docs", "world", "hero.blend"))
    alu = bpy.data.objects.get("Alu_root")
    print("HERO_BUILD", {"objects": len(WORLD.all_objects), "alu": tuple(round(c, 3) for c in alu.location) if alu else None,
                         "cam": tuple(round(c, 4) for c in CAM)})
