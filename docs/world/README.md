# World kit (Blender + key art)

The hero ("Arrival") is matched to the approved key art `inspo/Section_One.png` (1536 x 1024).
At rest the screen is the key art; when the pointer moves, real 3D geometry gives true
parallax, and Alu, the gate and the grass are live 3D.

## How it works

1. **The key art's camera.** `Hero_Cam` in `hero_build.py` (mirrored in `src/hero/heroCam.ts`)
   is a 34 mm lens on a 36 mm sensor, level, lens-shifted so the sea horizon sits on row 620.
   Its height and distance come from Alu: he is 1.35 m tall and 303 px tall in the key art.
2. **Far world: a matte painting.** `backdrop_build.py` cuts the sky, the big cloud, the
   headland with its crane and the sea out of the key art, paints out what the scene draws
   itself (UI, Alu, the gate, the pines, the foreground), rebuilds the sea row by row and pads
   the edges for parallax -> `public/images/hero/backdrop.webp`. The web maps it onto a dome at
   infinity by view direction (`Sky.tsx`), exactly as the rest camera saw it.
3. **Near world: projected proxies.** The same script writes `public/images/hero/plate.webp`:
   the foreground (terrace, step, ground, rocks, pines, the gate frame) with Alu, the gold
   tufts and the "scroll" label painted out. `hero_build.py` builds rough proxy meshes
   (material `Proj`) placed by back-projecting key-art pixels (`img_ground`, `img_depth`), and
   the web paints them by projecting the plate from the rest camera (`injectProjection` in
   `src/hero/shaders.ts`). Pines sway and keep their paint (the projection reads the rest pose).
4. **Live 3D.** Alu (`docs/robot/alu_v2.blend`), the gate glass and light, and the gold and
   green tufts (built to the painted tufts' sizes, paint baked into vertex colours).

## Files

| File | What it is |
|---|---|
| `backdrop_build.py` | Key art -> `backdrop.webp` (far world) and `plate.webp` (near world), plus `renders/pines.json` (pine silhouettes per row, read by `hero_build.py`). Needs numpy + Pillow. |
| `hero_build.py` | Builds the proxies, gate, tufts, places Alu, sets the camera; bakes per-vertex plate colours (the web's fallback where the hero camera cannot see); exports `public/models/world/hero.glb`; renders `renders/coverage.png`. |
| `hero.blend` | The saved result of `hero_build.py` with Alu placed. Rebuild with the script rather than editing by hand. |
| `renders/hero_web.png` | The web hero at rest (headless Chrome, 1536 x 1024), for comparing with the key art. |
| `renders/hero_arrival.png`, `hero_v1..v3.png` | The first, fully modelled attempt (before matching the key art). Kept for reference. |

## Rebuild

```bash
python docs/world/backdrop_build.py
"C:/Program Files/Blender Foundation/Blender 5.1/blender.exe" --background --factory-startup --python docs/world/hero_build.py
```

Run them in that order (the Blender script reads `plate.webp` and `pines.json`). Debug images
land in `renders/` (`backdrop_debug.png`, `plate_debug.png` with the masks outlined, and
`coverage.png`, the proxies' silhouette from the hero camera); they are not committed.

Checking the fit: the proxies must cover every foreground pixel of the plate (anything they
miss shows the backdrop's sea or sky there), and should not reach far past it. Compare
`coverage.png` against the plate's foreground.

## Coordinates

Blender: metres, Z up, the camera at -Y looking toward +Y, the gate's base centre at x = y = 0,
the terrace top at z = 0.181 where the gate and Alu stand, the ground in front of the step at
z = 0. On the web (Y up) Blender (x, y, z) is three.js (x, z, -y): the camera rests at
(0, 0.8384, 7.17).

## Changing the scene

Small moves of props are fine: the projection follows the geometry. A different composition
needs a new key art (and the masks and placements in both scripts re-measured), or the
proxies replaced by fully modelled and lit props like the first attempt.
