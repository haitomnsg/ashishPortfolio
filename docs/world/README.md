# World kit (Blender)

Blender sources for the 3D world. Every scene is built by a script, so changes are re-runs
and the `.blend` files are always reproducible. Blender 5.1.

| File | What it is |
|---|---|
| `hero_build.py` | Builds the Arrival (hero) world: ground, plateau and steps, cliff and sea, the glass gate with its light cards, pines, rocks, grass tufts, clouds, the hazy headland and crane, sun, sky, camera and render settings. Appends Alu (waving pose) from `../robot/alu_v2.blend`. |
| `hero.blend` | The saved result of `hero_build.py` with Alu placed. Open it to tweak by hand, or re-run the script from the Scripting tab to rebuild from scratch (idempotent: it replaces the `Hero_World` collection). |
| `renders/hero_arrival.png` | Reference render (EEVEE, Standard view transform, 1536 x 1024) used to match the web scene. `hero_v1..v3.png` are the iterations that led to it. |

## Export to the web

In Blender, after running the build script, run `export_world()` (defined at the bottom of
the script; also run automatically when the script is executed through the MCP bridge).
It writes `public/models/world/hero.glb` with:

- every prop as a named node (`Gate_Glass`, `Cloud_Main`, `Tuft_Gold_03`, `Sea`, ...) so
  `src/hero/World.tsx` can swap materials and animate pieces by name;
- vertex colours in `COLOR_0` (the `Col` attribute), linear, one matte material
  (`World_Paint`) for the whole kit plus `Gate_Glass`, `Gate_Light`, `Sea` and `Cloud`;
- modifiers applied, Y up, no lights or cameras (the web has its own).

Alu is not in this file; the web loads `public/models/alu.glb` (see `../robot/`).

## Coordinates

Blender: metres, Z up, the visitor at -Y looking toward +Y, the sea beyond the cliff at +Y,
ground in front of the steps at z = 0, the plateau top at z = 0.5 where the gate stands.
On the web (Y up) the same scene has the camera at +Z: Blender (x, y, z) is three.js
(x, z, -y). The web camera `CameraRig.tsx` mirrors `Hero_Cam` (34 mm lens).

## Palette

Colours live in `PAL` at the top of `hero_build.py` and follow `docs/DESIGN.md` section 3.
Facets get a small per-face value jitter so flat colours read as hand-painted.
