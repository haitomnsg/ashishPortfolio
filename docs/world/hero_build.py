# Builds the hero ("Arrival") world for the portfolio: a sunlit limestone plateau on a cliff
# above the sea, a tall glass gate on two wide steps, pines, rocks, grass, one big faceted
# cloud, a hazy headland with an old crane, sky and sun (DESIGN.md section 8).
# Stylized low-poly: simple volumes, hard faceted edges, flat vertex colours, one matte
# vertex-colour material for the whole kit (World_Paint) plus glass, light and sea.
#
# Idempotent: rerunning removes and rebuilds the "Hero_World" collection. Alu is appended
# from docs/robot/alu_v2.blend (waving pose) into "Alu" if that collection is missing.
# Run from Blender's Scripting tab, or exec() it through the MCP bridge. Blender 5.1.
#
# Coordinates: metres, Z up. The visitor (camera) is at -Y looking toward +Y; the sea is
# beyond the cliff at +Y. Alu faces -Y. Ground level in front of the steps is z = 0.
#
# Export: run export_world() (bottom) to write public/models/world/hero.glb with every
# prop as a named node, so the web can animate the cloud, sea, grass, gate light...
import bpy, bmesh, math, random, os
from mathutils import Vector, noise

R = math.radians
SC = bpy.context.scene
ROOT = r"D:\AshishPortfolio"
if bpy.data.filepath:
    cand = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), "..", ".."))
    if os.path.isdir(os.path.join(cand, "docs")):
        ROOT = cand


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
C_BACK = new_col("Backdrop", WORLD)
C_RIG = new_col("Rig", WORLD)          # camera, lights


# ---------------------------------------------------------------- palette + materials
def lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


PAL = {
    "stone":      "#F4EAD8",   # limestone, lit top faces
    "stone_side": "#E2D2B4",   # limestone side faces (sandy)
    "sand":       "#DCC8A6",   # sandy ground between things
    "path":       "#CF6E3A",   # red-ochre earth path
    "path2":      "#E08A52",   # lighter dust on the path
    "grass":      "#9DB64E",   # sunlit grass patch
    "grass2":     "#78953F",   # grass in the shade
    "pine":       "#4F6B3A",   # pine foliage
    "pine2":      "#6E8C46",   # pine tier tops
    "trunk":      "#7A4B2E",
    "gold":       "#F5A93A",   # dry golden grass tufts
    "gold2":      "#FFBA6F",
    "cloud":      "#FFFFFF",
    "cloud2":     "#E4EEF8",   # cloud underside, sky-tinted
    "frame":      "#FFFCF7",   # gate frame
    "head":       "#7E98BE",   # headland in haze
    "head2":      "#9DB5D4",
    "crane":      "#6C86AD",
    "sea":        "#55D9D0",
    "sea_far":    "#7FD9C4",
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
    "paint": make_mat("World_Paint", "#FFFFFF", rough=0.92, spec=0.22, vcol=True),
    "glass": make_mat("Gate_Glass", "#DDF4FF", rough=0.05, spec=0.6, alpha=0.16,
                      transmission=0.9),
    "light": make_mat("Gate_Light", "#FFF4D6", rough=1.0, spec=0.0, emit="#FFF1C9",
                      strength=1.4, alpha=0.10),
    "sea":   make_mat("Sea", PAL["sea"], rough=0.35, spec=0.5, vcol=True),
    "cloud": make_mat("Cloud", "#FFFFFF", rough=1.0, spec=0.0, vcol=True, emit="#FFFFFF", strength=0.55),
}


# ---------------------------------------------------------------- geometry helpers
def link_obj(name, data, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), col=None,
             parent=None):
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


def paint(o, hexc, jitter=0.03, seed=None):
    """Flat colour per face with a small value jitter: hand-coloured facets."""
    rnd = random.Random(seed if seed is not None else o.name)
    me = o.data
    attr = ensure_col_attr(me)
    base = Vector(lin(hexc)[:3])
    for p in me.polygons:
        k = 1.0 + rnd.uniform(-jitter, jitter)
        for li in p.loop_indices:
            attr.data[li].color = (base.x * k, base.y * k, base.z * k, 1.0)


def paint_fn(o, fn, jitter=0.03, seed=None):
    """fn(face_centre_world, face_normal_world) -> hex; per-face jitter on top."""
    rnd = random.Random(seed if seed is not None else o.name)
    me = o.data
    attr = ensure_col_attr(me)
    bpy.context.view_layer.update()
    mw = o.matrix_world
    for p in me.polygons:
        c = mw @ p.center
        n = (mw.to_3x3() @ p.normal).normalized()
        base = Vector(lin(fn(c, n))[:3])
        k = 1.0 + rnd.uniform(-jitter, jitter)
        for li in p.loop_indices:
            attr.data[li].color = (base.x * k, base.y * k, base.z * k, 1.0)


def mix(h1, h2, t):
    a, b = lin(h1), lin(h2)
    t = max(0.0, min(1.0, t))

    def s(c):  # linear -> sRGB hex component
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        return int(round(c * 255))
    return "#%02X%02X%02X" % tuple(s(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_bevel(o, width, segs=1):
    md = o.modifiers.new("Bevel", "BEVEL")
    md.width, md.segments = width, segs
    md.limit_method = "NONE"
    md.harden_normals = False
    return md


def box(name, loc, dims, hexc, col=None, bevel=0.0, rot=(0, 0, 0), jitter=0.03, parent=None,
        mat="paint"):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    o = link_obj(name, flat_mesh(bm, name), M[mat], loc, rot, col=col, parent=parent)
    if bevel:
        add_bevel(o, bevel, 2)
    paint(o, hexc, jitter)
    return o


def hash_noise(x, y, scale=1.0, seed=0):
    return noise.noise(Vector((x * scale + seed * 13.1, y * scale + seed * 7.7, seed * 3.3)))


# ---------------------------------------------------------------- ground
def ground():
    """A 44 x 30 m slab of faceted ground. z=0 near the path, gentle lumps elsewhere;
    the back edge (y = 8) is the cliff top."""
    bm = bmesh.new()
    XN, YN = 44, 30
    bmesh.ops.create_grid(bm, x_segments=XN, y_segments=YN, size=1.0)
    rnd = random.Random(21)
    for v in bm.verts:
        x, y = v.co.x * 22.0, v.co.y * 14.25 - 7.75   # x in [-22,22], y in [-22, 6.5]
        jx, jy = rnd.uniform(-0.28, 0.28), rnd.uniform(-0.28, 0.28)
        if abs(v.co.x) > 0.99 or abs(v.co.y) > 0.99:
            jx = jy = 0.0
        x, y = x + jx, y + jy
        lump = max(0.0, (abs(x) - 2.2) / 6.0)
        lump = min(lump, 1.0) * (0.55 * hash_noise(x, y, 0.22, 1) + 0.3)
        z = max(0.0, lump) * 0.9
        if y < -8:
            z += (-8 - y) * 0.015
        v.co = Vector((x, y, z))
    o = link_obj("Ground", flat_mesh(bm, "Ground"), M["paint"], col=C_GROUND)

    def colour(c, n):
        x, y = c.x, c.y
        edge = hash_noise(x, y, 0.55, 3) * 0.9
        w = 1.05 + max(0.0, (-y - 2.0)) * 0.11 + edge * 0.4
        if y < -1.9 and abs(x) < w:
            return mix(PAL["path"], PAL["path2"], 0.5 + 0.5 * hash_noise(x, y, 0.7, 4))
        g = hash_noise(x, y, 0.16, 5) + 0.25 * hash_noise(x, y, 0.6, 6)
        if abs(x) > w + 0.4 and g > 0.12:
            t = min(1.0, (g - 0.12) * 3)
            return mix(PAL["grass2"] if n.z < 0.92 else PAL["grass"], PAL["grass"], 0.3 + 0.4 * t)
        if n.z < 0.88:
            return PAL["stone_side"]
        return mix(PAL["sand"], PAL["stone"], 0.35 + 0.5 * hash_noise(x, y, 0.3, 7))
    paint_fn(o, colour, 0.035, 2)
    return o


def plateau():
    """The limestone slab the gate stands on (irregular faceted outline) and two wide
    steps down to the path."""
    rnd = random.Random(5)
    pts = []
    n = 18
    for i in range(n):
        a = i / n * math.tau
        rx, ry = 5.2 + rnd.uniform(-0.5, 0.5), 3.0 + rnd.uniform(-0.3, 0.3)
        pts.append(Vector((math.cos(a) * rx, math.sin(a) * ry + 1.6, -0.4)))
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in pts]
    bottom = bm.faces.new(vs)
    res = bmesh.ops.extrude_face_region(bm, geom=[bottom])
    extv = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=extv, vec=(0, 0, 0.9))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    topf = [f for f in bm.faces if f.normal.z > 0.9]
    bmesh.ops.poke(bm, faces=topf, offset=0.02)
    o = link_obj("Plateau", flat_mesh(bm, "Plateau"), M["paint"], col=C_GROUND)
    paint_fn(o, lambda c, n: PAL["stone"] if n.z > 0.6 else PAL["stone_side"], 0.03, 5)

    s1 = box("Step_Lower", (0.15, -2.55, 0.11), (7.4, 1.5, 0.23), PAL["stone"], C_GROUND, bevel=0.03)
    s2 = box("Step_Upper", (-0.1, -1.55, 0.31), (6.2, 1.3, 0.25), PAL["stone"], C_GROUND, bevel=0.03)
    for s in (s1, s2):
        paint_fn(s, lambda c, n: PAL["stone"] if n.z > 0.5 else PAL["stone_side"], 0.025, s.name)
    return o


def cliff_and_sea():
    """The cliff face behind the plateau dropping to the sea, and the sea plane as a coarse
    grid so its facets can shimmer on the web."""
    bm = bmesh.new()
    rnd = random.Random(9)
    cols = 44
    rows = [(6.5, 0.0), (7.1, -0.6), (7.9, -2.2), (8.7, -4.4), (9.5, -7.0)]
    grid = []
    for (y, z) in rows:
        row = []
        for i in range(cols + 1):
            x = -22 + 44 * i / cols
            jy = rnd.uniform(-0.25, 0.25) if 0 < i < cols else 0
            jz = rnd.uniform(-0.25, 0.25) if z < 0 else 0
            row.append(bm.verts.new(Vector((x, y + jy, z + jz))))
        grid.append(row)
    for r in range(len(rows) - 1):
        for i in range(cols):
            bm.faces.new((grid[r][i], grid[r][i + 1], grid[r + 1][i + 1], grid[r + 1][i]))
    o = link_obj("Cliff", flat_mesh(bm, "Cliff"), M["paint"], col=C_GROUND)
    paint_fn(o, lambda c, n: mix(PAL["stone_side"], PAL["sand"],
                                 0.5 + 0.5 * hash_noise(c.x, c.z, 0.4, 2)), 0.04, 9)

    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=60, y_segments=30, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 160.0, v.co.y * 80.0 + 86.0, -6.5))
    sea = link_obj("Sea", flat_mesh(bm, "Sea"), M["sea"], col=C_BACK)
    paint_fn(sea, lambda c, n: mix(PAL["sea"], PAL["sea_far"],
                                   min(1.0, max(0.0, (c.y - 8) / 120.0))), 0.02, 3)
    return o, sea


# ---------------------------------------------------------------- gate
def rounded_rect(w, h, r, n=5):
    """Points of a rounded rectangle in XZ, centred at x=0, from z=0 to z=h."""
    pts = []
    cx, cz = w / 2 - r, h - r
    corners = [(cx, cz, 0), (-cx, cz, 90), (-cx, r, 180), (cx, r, 270)]
    for (px, pz, a0) in corners:
        for i in range(n + 1):
            a = R(a0 + 90 * i / n)
            pts.append(Vector((px + math.cos(a) * r, 0.0, pz + math.sin(a) * r)))
    return pts


def gate():
    W, H, T, D = 2.2, 4.0, 0.08, 0.12     # width, height, frame thickness, depth
    base_z = 0.5                            # plateau top
    outer = rounded_rect(W, H, 0.20)
    inner = [p + Vector((0, 0, T)) for p in rounded_rect(W - 2 * T, H - 2 * T, 0.13)]
    bm = bmesh.new()
    vo = [bm.verts.new(p + Vector((0, -D / 2, 0))) for p in outer]
    vi = [bm.verts.new(p + Vector((0, -D / 2, 0))) for p in inner]
    n = len(vo)
    faces = [bm.faces.new((vo[i], vo[(i + 1) % n], vi[(i + 1) % n], vi[i])) for i in range(n)]
    res = bmesh.ops.extrude_face_region(bm, geom=faces)
    ev = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ev, vec=(0, D, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    frame = link_obj("Gate_Frame", flat_mesh(bm, "Gate_Frame"), M["paint"], (0, 0, base_z), col=C_GATE)
    add_bevel(frame, 0.012, 2)
    paint(frame, PAL["frame"], 0.015)

    bm = bmesh.new()
    vs = [bm.verts.new(p + Vector((0, 0, T))) for p in rounded_rect(W - 2 * T, H - 2 * T, 0.13)]
    bm.faces.new(vs)
    glass = link_obj("Gate_Glass", flat_mesh(bm, "Gate_Glass"), M["glass"], (0, 0, base_z), col=C_GATE)
    for p in glass.data.polygons:
        p.use_smooth = True

    bm = bmesh.new()
    a = [bm.verts.new(Vector(p)) for p in ((-0.9, -0.1, 0.01), (0.9, -0.1, 0.01),
                                              (1.9, -4.2, 0.01), (-1.9, -4.2, 0.01))]
    bm.faces.new(a)
    shaft = link_obj("Gate_LightShaft", flat_mesh(bm, "Gate_LightShaft"), M["light"], (0, 0, base_z), col=C_GATE)
    bm = bmesh.new()
    b = [bm.verts.new(Vector(p)) for p in ((-0.95, 0.35, 0.1), (0.95, 0.35, 0.1),
                                              (0.95, 0.35, 3.9), (-0.95, 0.35, 3.9))]
    bm.faces.new(b)
    haze = link_obj("Gate_Haze", flat_mesh(bm, "Gate_Haze"), M["light"], (0, 0, base_z), col=C_GATE)
    box("Gate_Sill", (0, 0, base_z + 0.015), (2.6, 0.6, 0.03), PAL["stone"], C_GATE, bevel=0.01)
    return frame, glass, shaft, haze


# ---------------------------------------------------------------- props
def pine(name, loc, h, seed, tiers=4, lean=0.0):
    rr = random.Random(seed)
    bm = bmesh.new()
    trunk_h = h * 0.32
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=h * 0.045, radius2=h * 0.03,
                          depth=trunk_h)
    for v in bm.verts:
        v.co.z += trunk_h / 2
    me_trunk = flat_mesh(bm, name + "_trunk")
    bm = bmesh.new()
    z = h * 0.22
    tier_h = (h - z) / tiers * 1.25
    for t in range(tiers):
        k = 1.0 - t / tiers
        rad = h * (0.26 * k + 0.07) * rr.uniform(0.9, 1.1)
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=rad, radius2=0.02,
                                     depth=tier_h)
        cx, cy = rr.uniform(-0.08, 0.08) * h, rr.uniform(-0.08, 0.08) * h
        for v in geom["verts"]:
            v.co.x *= rr.uniform(0.85, 1.15)
            v.co.y *= rr.uniform(0.85, 1.15)
            v.co += Vector((cx, cy, z + tier_h / 2))
        z += tier_h * 0.62
    me_fol = flat_mesh(bm, name + "_foliage")
    o_f = link_obj(name, me_fol, M["paint"], loc, (R(lean), 0, rr.uniform(0, 6.28)))
    o_t = link_obj(name + "_Trunk", me_trunk, M["paint"], loc, (0, 0, rr.uniform(0, 6.28)))
    paint(o_t, PAL["trunk"], 0.04, seed)
    paint_fn(o_f, lambda c, n: mix(PAL["pine"], PAL["pine2"], max(0.0, n.z) * 0.9), 0.05, seed)
    return o_f


def rock(name, loc, r, scale, seed):
    rr = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
    for v in bm.verts:
        v.co *= rr.uniform(0.78, 1.18)
        if v.co.z < 0:
            v.co.z *= 0.25
    o = link_obj(name, flat_mesh(bm, name), M["paint"], loc, (0, 0, rr.uniform(0, 6.28)), scale)
    paint_fn(o, lambda c, n: mix(PAL["stone_side"], PAL["stone"], 0.25 + 0.75 * max(0.0, n.z)),
             0.05, seed)
    return o


def tuft(name, loc, h, seed, blades=9, hexc=("gold", "gold2"), spread=0.9):
    """Dry grass: tall thin blades leaning out from a point. The vertex colour fades darker
    at the base. On the web, a vertex's height above the base is its bend weight."""
    rr = random.Random(seed)
    bm = bmesh.new()
    for i in range(blades):
        a = i / blades * math.tau + rr.uniform(-0.3, 0.3)
        lean = rr.uniform(0.35, 0.75) * spread
        bh = h * rr.uniform(0.6, 1.0)
        w = 0.025 + bh * 0.08
        d = Vector((math.cos(a), math.sin(a), 0))
        side = Vector((-d.y, d.x, 0)) * w
        base = d * 0.02
        tip = base + d * lean * bh + Vector((0, 0, bh))
        mid = base + d * lean * bh * 0.45 + Vector((0, 0, bh * 0.55))
        v0, v1 = bm.verts.new(base - side), bm.verts.new(base + side)
        v2, v3 = bm.verts.new(mid + side * 0.7), bm.verts.new(mid - side * 0.7)
        v4 = bm.verts.new(tip)
        bm.faces.new((v0, v1, v2, v3))
        bm.faces.new((v3, v2, v4))
    me = flat_mesh(bm, name)
    o = link_obj(name, me, M["paint"], loc, (0, 0, rr.uniform(0, 6.28)))
    attr = ensure_col_attr(me)
    c0, c1 = Vector(lin(PAL[hexc[0]])[:3]), Vector(lin(PAL[hexc[1]])[:3])
    for p in me.polygons:
        for li in p.loop_indices:
            vz = me.vertices[me.loops[li].vertex_index].co.z
            t = min(1.0, vz / max(h, 0.01))
            c = c0.lerp(c1, 0.25 + 0.75 * t) * (0.55 + 0.45 * t)
            attr.data[li].color = (c.x, c.y, c.z, 1.0)
    return o


def cloud(name, loc, seed, scale=1.0):
    rr = random.Random(seed)
    bm = bmesh.new()
    puffs = [((0, 0, 0), 5.2), ((3.6, 0.5, 1.0), 4.0), ((-3.4, 0.3, 1.4), 3.6), ((1.2, -0.4, 4.2), 3.8),
             ((-1.4, 0.6, 3.6), 3.2), ((5.8, 0.2, -0.6), 2.8), ((-5.6, 0.1, -0.8), 2.6),
             ((0.6, 0.3, 7.3), 2.6), ((2.8, -0.2, 6.2), 2.2)]
    for (c, r) in puffs:
        geom = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
        for v in geom["verts"]:
            v.co *= rr.uniform(0.86, 1.12)
            v.co += Vector(c)
    for v in bm.verts:
        if v.co.z < -2.0:
            v.co.z = -2.0 + (v.co.z + 2.0) * 0.3
    o = link_obj(name, flat_mesh(bm, name), M["cloud"], loc, (0, 0, 0), (scale,) * 3, col=C_BACK)
    zs = [v.co.z for v in o.data.vertices]
    lo, hi = min(zs), max(zs)
    span = max(1.0, (hi - lo) * scale)
    paint_fn(o, lambda c, n: mix(PAL["cloud2"], PAL["cloud"],
                                 0.2 + 0.45 * max(0.0, n.z) + 0.45 * ((c.z - loc[2] - lo * scale) / span)),
             0.02, seed)
    return o


def headland():
    """A far, hazy headland on the right: a few flattened faceted hills, and an old harbour
    crane on the highest one."""
    rr = random.Random(31)
    bm = bmesh.new()
    hills = [((0, 0, 0), 14.0, (2.6, 1.3, 0.55)), ((22, 3, 0), 11.0, (2.2, 1.2, 0.42)),
             ((-20, 2, 0), 9.0, (2.0, 1.1, 0.35)), ((8, -4, 0), 7.0, (1.6, 1.0, 0.5)),
             ((38, 1, 0), 7.0, (1.8, 1.0, 0.3)), ((-34, 4, 0), 6.0, (1.6, 1.0, 0.25))]
    for (c, r, sc) in hills:
        geom = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
        for v in geom["verts"]:
            v.co.x *= sc[0] * rr.uniform(0.92, 1.08)
            v.co.y *= sc[1] * rr.uniform(0.92, 1.08)
            v.co.z *= sc[2] * rr.uniform(0.9, 1.1)
            if v.co.z < 0:
                v.co.z *= 0.2
            v.co += Vector(c)
    o = link_obj("Headland", flat_mesh(bm, "Headland"), M["paint"], (44.0, 118.0, -7.2), (0, 0, R(-8)),
                 (1.0, 1.0, 1.0), col=C_BACK)
    paint_fn(o, lambda c, n: mix(PAL["head"], PAL["head2"], 0.35 + 0.65 * max(0.0, n.z)), 0.025, 31)
    cr = Vector((40.0, 114.0, -7.2 + 7.4))
    k = 0.55
    for nm, off, dims in (("Crane_Tower", (0, 0, 3.6), (0.6, 0.6, 7.2)), ("Crane_Boom", (-3.4, 0, 7.3), (9.0, 0.5, 0.45)),
                          ("Crane_Cab", (0.3, 0, 6.6), (1.4, 1.2, 1.0)), ("Crane_Cable", (-6.8, 0, 4.5), (0.12, 0.12, 5.6)),
                          ("Crane_Hook", (-6.8, 0, 1.6), (0.6, 0.5, 0.5)), ("Crane_Legs", (0, 0, 0.3), (1.6, 1.6, 0.6))):
        box(nm, cr + Vector(off) * k, tuple(d * k for d in dims), PAL["crane"], C_BACK, jitter=0.0)
    return o


# ---------------------------------------------------------------- build the scene
ground()
plateau()
cliff_and_sea()
gate()

pine("Pine_L", (-6.6, 2.4, 0.2), 5.2, 41, tiers=5, lean=2.0)
pine("Pine_R", (7.2, 1.6, 0.1), 4.6, 42, tiers=4, lean=-1.5)
pine("Pine_R2", (10.4, 5.0, 0.0), 3.4, 43, tiers=4)

rock("Rock_FL", (-4.4, -7.2, 0.0), 1.5, (1.7, 1.2, 0.95), 51)
rock("Rock_FL2", (-5.6, -3.6, 0.0), 1.2, (1.4, 1.0, 0.8), 52)
rock("Rock_FR", (4.9, -7.6, 0.0), 1.6, (1.6, 1.2, 0.95), 53)
rock("Rock_FR2", (6.0, -3.6, 0.0), 1.1, (1.4, 1.0, 0.7), 54)
rock("Rock_BL", (-4.6, 3.6, 0.3), 0.9, (1.4, 1.0, 0.7), 55)
rock("Rock_BR", (5.2, 3.9, 0.3), 1.0, (1.5, 1.1, 0.65), 56)
rock("Rock_M", (2.6, -3.4, 0.0), 0.3, (1.3, 1.0, 0.6), 57)

tufts = [((-3.3, -4.6, 0.0), 0.55, 61), ((-2.9, -2.4, 0.08), 0.5, 62), ((3.4, -3.2, 0.0), 0.6, 63),
         ((4.2, -5.6, 0.0), 0.5, 64), ((-5.0, -7.0, 0.0), 0.45, 65), ((2.4, -7.6, 0.0), 0.5, 66),
         ((-1.9, -6.9, 0.0), 0.35, 67), ((-4.2, 2.2, 0.5), 0.45, 68), ((3.6, 2.6, 0.5), 0.5, 69),
         ((6.0, -1.6, 0.05), 0.55, 70), ((-6.6, -0.8, 0.1), 0.5, 71)]
for i, (loc, h, s) in enumerate(tufts):
    tuft("Tuft_Gold_%02d" % i, loc, h, s)
green = [((-3.9, -3.5, 0.02), 0.26, 81), ((3.1, -4.6, 0.0), 0.24, 82), ((-2.3, -8.4, 0.0), 0.22, 83),
         ((4.9, -2.2, 0.0), 0.28, 84), ((-6.0, -2.0, 0.05), 0.24, 85), ((1.9, -9.2, 0.0), 0.2, 86)]
for i, (loc, h, s) in enumerate(green):
    tuft("Tuft_Green_%02d" % i, loc, h, s, blades=7, hexc=("grass2", "grass"), spread=0.7)

cloud("Cloud_Main", (12.0, 215.0, 46.0), 91, scale=3.6)
cloud("Cloud_Far_L", (-150.0, 300.0, 34.0), 92, scale=1.8)
cloud("Cloud_Far_R", (170.0, 320.0, 28.0), 93, scale=1.4)
headland()


# ---------------------------------------------------------------- Alu
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
        root.location = (-1.5, -0.35, 0.5)
        root.rotation_euler = (0, 0, R(28))     # body angled toward the gate, face to the visitor
    return root


place_alu()
purge_collection("Alu_Stage")


# ---------------------------------------------------------------- light, world, camera, render
sun_d = bpy.data.lights.new("Sun", "SUN")
sun_d.energy = 4.2
sun_d.angle = R(6)
sun_d.color = lin("#FFE3BC")[:3]
sun = link_obj("Sun", sun_d, col=C_RIG)
sun.rotation_euler = (Vector((0, 0, 0)) - Vector((-5.0, -3.2, 6.2))).to_track_quat("-Z", "Y").to_euler()

w = bpy.data.worlds.get("Hero_Sky") or bpy.data.worlds.new("Hero_Sky")
if w.node_tree is None:
    try:
        w.use_nodes = True
    except Exception:
        pass
nt = w.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld")
mixn = nt.nodes.new("ShaderNodeMixShader")
lp = nt.nodes.new("ShaderNodeLightPath")
amb = nt.nodes.new("ShaderNodeBackground")
amb.inputs[0].default_value = lin("#9DB4EA")
amb.inputs[1].default_value = 0.42
sky = nt.nodes.new("ShaderNodeBackground")
sky.inputs[1].default_value = 1.0
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.40
ramp.color_ramp.elements[0].color = lin("#CFEAF7")
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = lin("#3FA2DE")
nt.links.new(tc.outputs["Window"], sep.inputs[0])
nt.links.new(sep.outputs["Y"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], sky.inputs[0])
nt.links.new(lp.outputs["Is Camera Ray"], mixn.inputs["Fac"])
nt.links.new(amb.outputs[0], mixn.inputs[1])
nt.links.new(sky.outputs[0], mixn.inputs[2])
nt.links.new(mixn.outputs[0], out.inputs[0])
SC.world = w

cd = bpy.data.cameras.new("Hero_Cam")
cd.lens = 34
cd.sensor_width = 36
cd.clip_end = 1000
cam = link_obj("Hero_Cam", cd, loc=(0.3, -12.2, 2.0), col=C_RIG)
cam.rotation_euler = (Vector((0.1, 0.0, 2.05)) - cam.location).to_track_quat("-Z", "Y").to_euler()
SC.camera = cam

SC.render.engine = "BLENDER_EEVEE"
SC.render.resolution_x = 1536
SC.render.resolution_y = 1024
SC.render.resolution_percentage = 100
SC.eevee.taa_render_samples = 48
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
SC.render.use_compositing = False
SC.render.film_transparent = False
bpy.context.view_layer.update()


# ---------------------------------------------------------------- export
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


dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in WORLD.all_objects:
    if o.type == "MESH":
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        o.evaluated_get(dg).to_mesh_clear()
result = {"objects": len(WORLD.all_objects), "tris": tris, "alu": bpy.data.objects.get("Alu_root") is not None}
