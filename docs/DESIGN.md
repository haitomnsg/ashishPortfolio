# Design Direction — "Alu opens a door"

> The concrete visual identity for the portfolio, derived from `README.md` (the vision) and
> `docs/PROFILE.md` (the facts). `README.md` says *what it should feel like*; this file decides
> *what it is*. When the two disagree, README wins and this file gets fixed.

**History.** 2026-09-30: white "exhibition hall" direction, glossy robot (v1). 2026-10-03: moved to a
**stylized, sunlit sci-fi coast** in the spirit of *Caravan SandWitch*, with Alu redesigned to match
(v2). The white-world artifact and the white "Clean Room" lab environment are superseded. The Clean Room
UI principles that still hold are carried into §12.

## 0. One-line

A small cream-and-blue explorer robot stands beside a glass gate on a sunlit limestone coast, says one
line, and walks through into a stylized world of one engineer's work. Three paths in that world
(software, AI, robotics) start apart and braid into one.

## 1. Naming

- **World name (internal):** *The Threshold*. Never shown as a title; used in code and docs.
- **Robot name:** **Alu**, from Ashish's Instagram bio ("Kinda like Alu 🥔", *alu* = potato). It is the
  working name used on the model, the renders and the hero mockups (the speech bubble's name tag). An
  explicit final yes is still open (PROFILE §7).
- **Chapter names** are short nouns rendered in tiny mono labels, never marketing headlines.

## 2. The look: a stylized, sunlit coast

**Reference:** the art direction of *Caravan SandWitch* (Studio Plane Toast, 2024; art director Charles
Boury, write-up at charlesboury.fr/projets/caravan-sandwitch.html). It is a reference for *technique*,
never a source to copy.

| What the game does | What we do with it |
|---|---|
| Simple volumes, low-detail textures, few reusable materials (all the game's foliage comes from 39 props) | Every object is buildable from a few faceted shapes; flat vertex colours; a small prop kit reused everywhere |
| Grounds sci-fi in a real place (Provence: limestone, pines, turquoise sea, red earth) | Same Mediterranean coast mood. **Not Nepal** (Ashish decided 2026-10-03) |
| Hopeful post-apocalypse: old machines reclaimed by nature | Quiet cranes, antennas and containers in the landscape; never menacing |
| One iconic hero object (the yellow van); characters brighter and rounder than the world | Alu is the brightest, roundest thing in every frame |
| A small fixed palette; darkest shade is plum, never black | Fixed palettes below; shadows blue-violet, never black |
| Huge skies, low camera, small hero, lots of empty space | Same framing rules for every wide shot |
| A cool turquoise UI over a warm world; dialogue in white bubbles with a coloured name tag | Navy/cyan UI and glass chrome over the warm world; Alu speaks in a white bubble with a cyan name tag |
| A scan mode that tints the world teal and outlines tech | Our "evidence on focus" view (§11) |
| Same world in different moods: day, sandstorm, night | Light mode = day, dark mode = night on the same coast |

**Do not take:** the van, the characters, the game's locations, logo, typeface or menus.

## 3. Colour system

### World (3D scene)

| Role | Hex | Notes |
|---|---|---|
| Limestone, warm white | `#FFFCF7` (lit) · `#DCC8A6` (sandy ground) | ground, cliffs, rocks; per-face ±5% value jitter |
| Sky | `#3FA2DE` top → `#CFEAF7` horizon | camera-only gradient; scene lit by a flat sky colour |
| Sea | `#4BFFCA`, muted toward `#7FD9C4` | thin strip at the horizon |
| Pine / grass | `#556A39` | |
| Earth path | `#C4552E` | |
| Dry grass | `#FFBA6F` | |
| Shadow tint | sky fill `#9DB4EA` at low strength | shadows read blue-violet, never black |

Reference lighting (matches the Alu renders): sun `#FFE3BC`, strength 4.2, 6° soft angle, from the
upper left and front; sky fill `#9DB4EA` at 0.42. Renders use Blender's "Standard" view transform (not
AgX), which keeps colours flat and saturated; match that tone mapping on the web.

### Alu

| Part | Hex |
|---|---|
| Shell (cream-white) | `#F6EAD6` |
| Blue (limbs, ears, pelvis) | `#2A9EE0` |
| Dark (joints, soles, screen surround) | `#2C2547` · lighter dark `#433B63` |
| Orange accent (screws, straps, hubs, flag, lid) | `#FF9F1C` · shade `#E0711A` |
| Painted metal | `#B3B5C2` |
| Glow (eyes, lights, antenna, beacon) | `#7FE6FF` emissive |
| Dust on boots and wheels | `#C9A57E`, blended by height |

### Interface (2D over the 3D)

| Token | Light (day) | Dark (night) | Role |
|---|---|---|---|
| `--ink` | `#03045E` | `#F2FBFD` | text: navy, never black |
| `--ink-2` | `#4A5B7A` | `#A9C9D6` | secondary text, mono labels |
| `--paper` | `#FFFCF7` | `#0A1070` | case-study sheet, menu, speech bubble |
| `--line` | `#E6DCCB` | `#28338F` | hairlines |
| `--glass` | `rgba(255,252,247,.64)` + blur 20 px | `rgba(10,16,112,.58)` + blur 20 px | floating chrome only |
| `--cyan` | `#00B4D8` | `#00B4D8` | "powered" accent: name tag, active callout, progress |
| `--link` | `#0077B6` | `#48C6E6` | text links |
| `--focus` | `#0077B6` | `#00B4D8` | focus ring (cyan fails 3:1 on light) |
| `--accent` | `#FF9F1C` | `#FF9F1C` | non-text orange only |
| `--accent-ink` | `#B85109` | `#FFB45C` | the one highlighted word in a bubble (≈4.9:1 on day paper, ≈9:1 on night paper) |

Rules
- **Blue means powered.** Cyan appears only on things that are on: Alu's eyes and lights, the beacon,
  the gate's light, the focused callout, the active chart line, the name tag.
- **Orange is small.** Physical accents on Alu and one highlighted word per speech bubble. Never a
  fill for panels or buttons.
- No pure black anywhere. No gradients in the UI; light belongs to the 3D scene.
- The three domains are told apart by **place and props**, not by hue.
- Dark mode = the same coast at night: deep-blue sky, a few warm lamps, Alu's glow carries the frame.

## 4. Typography

One family, one mono for labels.

- **Primary: Geist Sans** (free, variable). Body 400, UI 500. Headline weight is still open: 500
  (quiet) or 600 (closer to Apple); 600 is recommended. Tracking −2 to −3.5% above 40 px.
  Fallback stack: `"Geist", "Inter Tight", system-ui, sans-serif`.
- **Labels: Geist Mono** at 11–12 px, uppercase, +8% tracking, `--ink-2`. Chapter names, dates, units,
  model and part names, the progress indicator, "SCROLL TO FOLLOW".
- **Speech bubble:** Geist 500, 18–20 px, `--ink` on `--paper`; one word in `--accent-ink`. Name tag:
  Geist Mono 11 px uppercase, navy on a cyan pill.
- Scale (desktop → mobile): display 88/48, h1 56/38, h2 36/26, body 18/17, small 14, label 12.
- Line length ≤ 62 ch. Case-study prose 18 px on a max-width 640 px column.
- No text shadows, no gradient text, no all-caps headlines.

## 5. Logo & motif

The existing monogram (a single geometric stroke inside a circle) stays unchanged. The wordmark
top-left is the mark plus "Ashish Gupta" in Geist 500. The earlier rule that turned the mark's 45°
strokes into the portal profile is dropped.

## 6. Alu v2 — character sheet (as built)

Files: `docs/robot/alu_v2_build.py` (rebuild script, run in Blender 5.1), `docs/robot/alu_v2.blend`
(waving hero pose), `public/models/alu.glb` (rest pose, about 665 KB before compression), renders in
`docs/robot/renders/alu_v2_hero.png` and `alu_v2_turnaround.png`. v1 sources stay in `docs/robot/` for
reference only.

- **Silhouette:** a big boxy head on a small body. Readable at 24 px. Head about 0.54 × 0.42 × 0.40 m;
  head top at 1.03 m; antenna tip 1.2 m; flag beacon 1.33 m. Faces −Y; his left is +X.
- **Head:** cream shell with chamfered faceted edges; a dark recessed screen with two big glowing oval
  eyes, thin scanlines across them and a small smile; four orange hex screws; an orange stripe above the
  screen; blue ear disks with orange rings; a dark carry handle; a back vent with blue slats.
- **Antenna** (left ear): straight metal rod, dark base, two collars (one orange), glowing tip.
- **Roof flag** (top rear right of the head): clamp block, short metal mast, orange collar, beacon on top,
  and a swallowtail cloth pennant (orange with a cream hoist band and centre stripe, faceted folds).
- **Body:** cream torso with a dark seam around a bolted chest plate: three cyan status lights, an orange
  button, speaker slots. Rubber bellows at the neck and waist. Blue pelvis with metal side caps.
- **Back:** a docked power pack: cream housing, orange lid, a charge meter with 3 of 4 bars lit, vent
  slats, two metal cells with blue bands, dock clamps, cables from the cells to the shoulders.
- **Arms:** cream shoulder pads with metal servo caps, dark upper arms and elbows, chunky blue forearms
  with a cyan glow ring, dark grippers with two grey fingers.
- **Legs:** dark hips and thighs, cream knee pads with servo caps, pistons on the back of each leg,
  chunky blue shins, cream boots with orange straps, thick dark soles, heel wheels with orange hubs,
  dust on the boots.
- **Materials (3 draw calls):** `Alu_Paint` (base colour from the `Col` vertex-colour attribute, matte,
  roughness .86), `Alu_Screen`, `Alu_Glow` (emissive). No texture maps.
- **Budget:** about 7.9k triangles (cap 25k). Compress with Draco or Meshopt in the asset step.
- **Rig:** pivot empties, not bones: `Alu_root`, `body`, `neck`, `head`, `antenna`, `arm_{L,R}_{1..3}`,
  `leg_{L,R}_{1..3}`. Heel wheels are meshes `wheel_L` / `wheel_R` that spin on their local Z. Rotate
  the empties to pose; all zero is the rest pose. The flag and antenna ride on `head`; the pack and its
  cables ride on `body`.
- **Locomotion:** walks on short legs; on flat ground he can lean back onto his heel wheels and roll.
- **Personality in motion:** curious (head leads, body follows about 120 ms later), polite (never blocks
  content, steps aside when a case study opens), proud after a project reveal (tiny chest-up). The flag
  sways with head turns. Idle: breathing scale ±1.5%, occasional look-around, slow beacon pulse.
- **Speech:** short authored lines in a bubble only (§10). No chat.
- **Clips:** `idle`, `look`, `walk`, `roll`, `turn`, `wave`, `point`, `present`, `enter`, `celebrate`,
  `sit`, `talk` (eyes and mouth flicker while a bubble is open).
- **Not:** WALL-E's binocular eyes, EVE's shape, a tracks + cube body, or any *Caravan SandWitch*
  character.

## 7. The gate

- A tall, thin **glass pane, 4.0 m × 2.2 m**, softly rounded corners, in a slim white frame (8 cm).
  It stands upright on the ground in the centre of the opening shot, about four times Alu's height.
- The glass reflects the sky. Light comes *through* it: a gentle shaft on the ground in front, light haze
  behind. When Alu steps in, the glass clears from the centre out.
- Reused at chapter changes and for every ★ project, at a smaller scale (a 1.6 m door for case studies),
  same profile every time.

## 8. Hero (Arrival) — spec

**Composition:** calm and nearly symmetric, camera at eye level and slightly low. The gate is in the
centre. Alu stands right beside it at its base (his body angled toward the gate, his head turned to the
visitor), waving with his outer hand. The sky fills the top half.

**Components** (the full model list for the first screen; keep it this small):

| Component | Build |
|---|---|
| Ground plateau | one faceted low-poly mesh: warm white limestone steps, a grass patch, a red-ochre path to the gate |
| Gate | frame + glass pane + light-shaft card |
| Alu | `public/models/alu.glb` |
| Pines ×2 | one mesh, instanced, not mirrored |
| Grass tufts ×3, rocks ×2–3 | one mesh each, instanced with random rotation and scale |
| Sea | a flat plane strip at the horizon |
| Headland + old crane | a flat silhouette card, faded by haze |
| Sky + one big faceted cloud | gradient backdrop + one low-poly cloud mesh or card |

**UI and copy** (nothing else on screen):
- Top-left: wordmark (monogram + "Ashish Gupta").
- Top-right: a glass pill with "Menu".
- A speech bubble above and left of Alu: name tag "ALU", line *"I wasn't the first thing he built."*,
  with "built" in `--accent-ink`.
- Bottom-centre: mono "SCROLL TO FOLLOW".

**Timing:** the scene is visible at once; Alu turns to the visitor at about 0.6 s; the bubble appears
at about 1.2 s. Scrolling starts the Threshold (§9).

## 9. The world map (chapters)

The chapter order holds. Their settings on the coast are **proposals** until designed.

```
[Arrival: gate on the cliff top]──gate──[Origins: three trails begin]──┬──> Robotics: a workshop hangar
                                                                       ├──> AI: an antenna / observatory station
                                                                       └──> Software: a small working harbour village
                                                  trails braid ──> [Crossroads: projects that use all three]
                                                               ──> [Record: timeline markers along the path]
                                                               ──> [Signal: dusk to night on the shore]
```

1. **Arrival** — the hero (§8).
2. **Threshold** — scroll walks Alu into the gate; the glass clears; the camera follows through. The
   only "blocking" moment; skippable (any key / tap / `Skip intro`).
3. **Origins** — three trails start at one point (Class 9). Alu: *"It started with two things at once:
   code and wires."*
4. **Domain places** — each domain is a place along the coast with 3–5 project artifacts. Alu walks the
   path; the camera tracks laterally. Hover lifts an artifact and shows a mono placard; click opens its
   small gate → case study.
5. **Crossroads** — the trails meet. TomatoBot and Phulbari live here (they need all three). The
   published paper is a glass-cased artifact.
6. **Record** — placements, the paper, the two schools and the two companies as markers along the path,
   in time order. Alu points at the current year.
7. **Signal** — the light falls to dusk, then night (dark mode); Alu sits on the shore. Email, phone,
   GitHub, LinkedIn as four mono lines; a minimal form.

Fallback route: a persistent `Menu` opens a plain, semantic, scrolling HTML version of the whole site
(same content source); `?flat=1` or `prefers-reduced-motion` loads it by default.

## 10. Alu's narration

- One line at a time, at most one per chapter, ≤ 10 words. First person (Alu speaking).
- Abstract, but every line points at something true (PROFILE.md). Nothing invented.
- He **never says Ashish's name**; he says "he". The name lives only in the wordmark and the page title.
- One highlighted word per line, in `--accent-ink`.
- Bubbles never block content, close on scroll, and appear as plain text in the flat route.
- Example lines: *"I wasn't the first thing he built."* (Arrival) · *"It started with two things at
  once: code and wires."* (Origins) · *"This one finds the ripe ones."* (TomatoBot) · *"This one learned
  to walk on its own."* (JeevI).

## 11. Case-study surface

When a project gate opens, the scene defocuses (haze + 40% dim) and a **single solid sheet** in
`--paper` slides in from the right (desktop 560 px, mobile full), with a glass "Esc · Close" chip.
Order inside is fixed: title → one-sentence problem → 3–5 images/video → "What I built" → "Decisions"
→ "Stack" (mono line) → "Result" → links. Alu stands beside the gate, idle. `Esc`/swipe closes. No
modals inside modals.

**Evidence on focus (scan view):** focusing an artifact tints the world slightly teal and outlines its
machines in cyan, like the game's scan mode. Then thin leader-line callouts name its parts and
dimensions in mono (four at most, horizontal or 45° leaders). Evidence comes from Ashish's CAD files
(Fusion 360, Blender, Isaac/URDF) and graphs redrawn in site style from the raw numbers.

## 12. Design language (kept from the Clean Room proposal)

- **The interface never jokes.** No emoji, stickers or bounce in the UI; Alu carries all the
  personality.
- **Evidence on focus** (§11).
- **Blue means powered** (§3).
- **Glass to steer, paper to read.** Glass only for one-line floating controls; anything you read sits on
  a solid sheet.
- **One soft shape family.** Rounded corners that scale with size (chip 8 · control 12 · panel 16 ·
  sheet 24 px is the recommended "balanced" scale, still to be confirmed); pills for buttons and chrome.
- **Smooth world, crisp instruments** (§13).

Clean Room artifact: https://claude.ai/artifact/DNne9E49r6MKVEniNcX6tD (source `docs/design/language.html`).
Its white lab environment no longer applies; its UI rules above do.

## 13. Motion rules

- Two clocks. World (camera, Alu): damped springs, 600–900 ms, no camera roll or shake, dolly and pan
  only, one move at a time. Instruments (chrome, labels, callouts, bubbles): 120–220 ms,
  `cubic-bezier(.2,.7,.2,1)`, no overshoot. Sheets: 320 ms.
- Only Alu (and his flag) may overshoot.
- Scroll drives a damped timeline (Lenis + a `useScrollProgress` store); the world catches up in
  ≤ 600 ms.
- Alu never moves faster than the camera can follow; if the visitor outruns him, he repositions during a
  cut, never on screen.
- Every animation ≤ 900 ms except the Threshold (2.4 s, skippable).
- `prefers-reduced-motion`: no camera dolly, crossfades instead, Alu static, flat route offered.

## 14. UI inventory (everything that may appear over the 3D)

Top-left: wordmark (home). Top-right: glass pill `Menu` · theme · sound. Bottom-left (after Arrival):
mono chapter label + vertical progress stroke. Bottom-centre: "SCROLL TO FOLLOW" (first screen only).
Alu's speech bubble when he speaks. Bottom-right: nothing. That is the whole chrome.

## 15. Do-not list (site-specific, beyond README §33)

No game UI (health bars, minimaps, quest markers, inventories, game menus); no photoreal or glossy
renders; nothing copied from *Caravan SandWitch* (van, characters, places, logo, type, menus); no skill
percentage bars; no tech-badge walls; no cards with drop-shadows in a grid; no "Hey 👋"; no typewriter
effect; no particles that do not come from a light source; no chat input on Alu (his bubble shows
authored lines only); no pure black.

## 16. References

- Type study: https://claude.ai/artifact/59JV5E8iFo7NQMdVQbMs3e (`docs/design/type.html`) — Geist still current.
- Superseded: white direction https://claude.ai/artifact/5k9aRuHorYkv4U9i9yzCDD (`docs/design/direction.html`).
- Inspo: `inspo/Glass_One.jpg`, `inspo/Glass_Two.jpg` (glass in landscape), `inspo/Robot_One.jpg`,
  `inspo/Robot_Two.jpg` (Alu's silhouette).
