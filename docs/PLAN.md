# Build Plan

> Turns `README.md` (vision) + `docs/DESIGN.md` (identity) + `docs/PROFILE.md` (facts) into a
> sequence of shippable milestones. Each milestone ends with something deployable, so the site is
> never "under construction" for long.
>
> **Updated 2026-10-03** for the stylized, sunlit coast direction (DESIGN §2) and the finished Alu v2
> model. The stack is unchanged; the art pipeline, world pieces and milestones changed.

## 1. Technical decisions

| Area | Decision | Why |
|---|---|---|
| Framework | **Vite + React 19 + TypeScript** | Static output suits the existing GitHub Pages setup; no server needed; fastest R3F iteration. Current site is already Vite. |
| 3D | **three.js + @react-three/fiber + @react-three/drei** | README §24; drei gives GLTF loading, instancing, `ScrollControls`-style hooks. The gate's glass is a cheap reflective material; `MeshTransmissionMaterial` only on the high tier. |
| Post-processing | `@react-three/postprocessing` (Bloom, N8AO/SSAO, Vignette) | Bloom for cyan emissives only; AO for contact depth on the faceted ground. No filmic tone mapping, to match the Blender "Standard" renders (DESIGN §3). Disabled on low tier. |
| World art | **Low-poly, flat vertex colours, hard faceted edges**, built in Blender from small scripted kits (like `docs/robot/alu_v2_build.py`) and exported as GLB | DESIGN §2/§8: every object buildable from a few shapes; one matte vertex-colour material per kit; repeated props instanced; distant sky/headland as flat backdrops. |
| Animation | **GSAP 3** (timelines, ScrollTrigger for DOM) + **Lenis** for smooth scroll + spring damping in `useFrame` for camera/robot | Scroll → one damped `progress` scalar drives everything; GSAP timelines for authored cinematic beats. |
| State | **Zustand** (`useJourney`: progress, chapter, activeProject, quality tier, theme, sound) | Tiny, works inside and outside the Canvas. |
| Routing | `react-router` with hash-less URLs; each chapter and project has a URL (`/work/tomatobot`) that seeks the journey to the right place | Deep-linkable case studies; fixes the current 404s. |
| Content | Typed data in `src/content/*.ts` (projects, timeline, awards), Markdown for case-study prose via `vite-plugin-md` or plain `.md?raw` + `marked` | One source feeds both the 3D world and the flat fallback site. No CMS. |
| Styling | CSS Modules + CSS custom properties from the interface tokens in `DESIGN.md §3` (no Tailwind) | The UI surface is small; tokens matter more than utilities. |
| Fonts | Geist Sans + Geist Mono, self-hosted, `font-display: swap`, subset latin | Single primary family per README §19. |
| Assets | GLB + Meshopt/Draco via `gltf-transform` in a `scripts/optimize-assets` step; vertex colours instead of textures (KTX2 only for photos and backdrops) | README §22. |
| Quality tiers | `low / mid / high` chosen from `navigator.hardwareConcurrency`, `devicePixelRatio`, WebGL renderer string, and a 1 s FPS probe; user can override | Mobile gets fewer lights, no post FX, capped DPR 1.5. |
| Accessibility | Flat semantic route (`/flat`) generated from the same content; `prefers-reduced-motion` and `?flat=1` auto-route there; every 3D interaction has a DOM twin | README §28. |
| Hosting | GitHub Pages first (add `404.html` SPA fallback + custom domain); move to Cloudflare Pages if bandwidth for GLBs becomes a problem | Keep what works today. |
| Tooling | pnpm, ESLint + Prettier, Vitest for content/schema tests, Playwright for smoke + screenshot tests, GitHub Actions deploy | |
| Robot model | **Done:** `public/models/alu.glb` (Alu v2, ~7.9k tris, 3 materials, rest pose). `<Alu />` loads it and drives the named pivot empties (`body`, `neck`, `head`, `antenna`, `arm_*`, `leg_*`, `wheel_*`, DESIGN §6) | No placeholder needed; animation code targets the real rig from day one. |

## 2. Repository layout

```
ashishPortfolio/
├── README.md                 vision (source of truth)
├── docs/                     PROFILE.md · DESIGN.md · PLAN.md · design/ (direction pages)
│                             robot/ (Alu build script, .blend, renders) · world/ (prop-kit build scripts, .blend)
├── public/                   fonts/ models/ (alu.glb, world/*.glb) images/ 404.html CNAME
├── scripts/                  optimize-assets.mjs · check-content.mjs
├── src/
│   ├── app/                  App.tsx · routes.tsx · providers
│   ├── content/              projects.ts · timeline.ts · awards.ts · profile.ts · narration.ts · md/*.md
│   ├── journey/              useJourney.ts (store) · chapters.ts (progress ranges) · cameraPath.ts
│   ├── scene/                Canvas root, lighting (sun + sky fill), quality tiers, postfx
│   │   ├── world/            Ground · Trails · Gate · Sea · Backdrop (sky, cloud, headland) · Places · Markers · Shore
│   │   ├── alu/              Alu.tsx (GLB loader) · rig.ts · behaviours/*.ts
│   │   ├── artifacts/        one component per ★ project + generic ArtifactPlinth
│   │   └── fx/               Haze · LightShaft · ScanView
│   ├── ui/                   Chrome (wordmark, menu, theme, sound) · SpeechBubble · ChapterLabel · Progress · Callouts · CaseStudySheet · Flat/*
│   ├── styles/               tokens.css · base.css · type.css
│   └── lib/                  math · easing · device · a11y
└── tests/                    content.spec.ts · smoke.spec.ts
```

## 3. Milestones

Estimates assume evenings/weekends. Each milestone has a definition of done (DoD).

### M0 — Foundation (2–3 days)
- Scaffold Vite/React/TS, pnpm, ESLint/Prettier, Vitest, Playwright, GitHub Actions → Pages.
- `styles/tokens.css` from DESIGN §3 (interface tokens, day + night), Geist self-hosted, base type scale.
- Content model + first pass of `projects.ts` populated from PROFILE §3 (12 projects, 6 with images).
- **Flat site** (`/flat`): home, work, work/:slug, about (timeline), record, contact. Fully semantic,
  keyboard-navigable, dark mode. This alone already replaces the current site's information.
- `404.html` SPA fallback so deep links work on GitHub Pages.
- DoD: deployed to a preview URL; Lighthouse a11y ≥ 95; all existing content reachable.

### M1 — Identity kit (2–3 days)
- **Done:** direction docs (`docs/design/`), Alu v2 model, turnaround and hero renders (`docs/robot/`).
- `<Alu />` GLB loader with the rig contract; idle + look behaviours driven by the pointer; flag sway.
- **Hero prop kit v1** in Blender (`docs/world/`), per DESIGN §8: ground plateau, gate (frame + glass +
  light-shaft card), pine, grass tuft, rock, cloud, headland-and-crane card. Flat vertex colours,
  exported to `public/models/world/`.
- Pick one ChatGPT hero mockup as the composition reference.
- DoD: a `/lab/alu` dev route shows Alu and the prop kit under the reference lighting (DESIGN §3) in
  day and night, and side-by-side matches the Blender renders.

### M2 — Arrival + Threshold (4–6 days) — *the hero*
- Scene root, quality tiers, lighting (warm sun + blue-violet sky fill + rim), faceted ground with
  contact shadows, haze.
- Gate glass (reflective; transmission on high tier), light shaft (cheap: layered additive planes),
  sky gradient backdrop, one cloud, sea strip, headland card.
- Scroll → damped progress store; GSAP master timeline for beats 0–1 (Alu turns to the visitor, speech
  bubble line, scroll → he walks into the gate, glass clears, camera follows through).
- Skip intro, reduced-motion crossfade, mobile framing (portrait camera path).
- Chrome: wordmark, Menu glass pill, theme, sound-off, "SCROLL TO FOLLOW", speech bubble.
- DoD: matches the chosen hero mockup's composition; 60 fps on a mid laptop at DPR 1.5, ≥ 30 fps on a
  2022 mid Android; first paint < 1.5 s on 4G (scene assets stream in behind a warm-white screen with
  the wordmark; no spinner).

### M3 — Journey spine (5–7 days)
- Camera path (Catmull-Rom) through the 7 chapters; `chapters.ts` maps progress ranges to labels,
  URLs, and camera keys.
- Alu locomotion along the trails: walk cycle, heel-wheel roll on flat stretches, lean into turns,
  head look-ahead, flag sway, repositioning during cuts.
- Narration: one authored bubble line per chapter from `content/narration.ts` (DESIGN §10).
- Origins: three trails from one point; three small artifacts.
- Domain places (robotics / AI / software) blocked out with the prop kit; settings per DESIGN §9 once
  decided; generic plinths for artifacts; hover lift + placard.
- Crossroads (trails braid); Record markers along the path; Signal on the shore with the day → night
  transition.
- DoD: whole journey scrollable end-to-end with placeholder artifacts; every chapter deep-linkable.

### M4 — Artifacts + case studies (6–8 days)
- `CaseStudySheet` (DOM) with the fixed content order; open/close choreography with scene defocus;
  `Esc`/swipe; URL sync.
- Scan view + callouts (DESIGN §11): teal world tint, cyan outlines on the focused artifact, up to four
  mono leader-line callouts.
- Hero artifacts (low-poly, vertex-coloured, ≤ 5k tris each), built from Ashish's real CAD where it
  exists (Fusion 360 → STEP/OBJ → Blender → GLB; JeevI from its URDF/STL in `jeevi-ii`, decimated and
  flat-shaded). Ideas still to confirm: TomatoBot (base + arm + a tomato), DocLipi (a document stack),
  Phulbari (a flower pot with a moisture probe), ArthaVidhi (a ledger), plus generic plinths for the rest.
- Charts redrawn from raw numbers (TensorBoard/CSV → JSON → SVG at build time).
- Image galleries from `public/images/` (screenshots and robot photos); Nepali product names kept.
- Alu behaviours: `present` (walks beside the gate, gestures), `celebrate` after a result line.
- DoD: 12 projects browsable in 3D and in flat; content parity test passes.

### M5 — Record + Signal (2–3 days)
- Timeline markers along the coastal path (2019 → 2027) for the 7 placements, the paper, schools,
  companies; Alu points at "now".
- Contact: mono lines + a minimal form (Formspree or a Cloudflare Worker; no backend to maintain),
  privacy note, success state where Alu waves.
- DoD: all PROFILE §2 facts present and correct; form delivers to haitomns@gmail.com.

### M6 — Polish, performance, accessibility (4–5 days)
- Asset pipeline (Meshopt/Draco; KTX2 for photos and backdrops), lazy chapter loading with `Suspense`
  boundaries, preloading the next chapter's assets on idle.
- Mobile pass: portrait camera paths, touch scroll, tier `low` visuals, text sizing.
- A11y pass: focus order over the Canvas, live region for chapter changes, DOM twins audited,
  screen-reader run-through of `/flat`.
- SEO: per-route titles/meta/OG images (rendered from the scene), sitemap, JSON-LD Person.
- Sound (optional, off by default): wind/sea ambience + 5 tiny samples (step, roll, gate, hover, open).
- DoD: Lighthouse perf ≥ 85 desktop / ≥ 70 mobile on the 3D route, 95+ on flat; no CLS.

### M7 — Alu animation (parallel track)
- **Model done 2026-10-03** (Alu v2, DESIGN §6; `public/models/alu.glb`, about 665 KB before compression).
- Clips from DESIGN §6 (`idle`, `look`, `walk`, `roll`, `turn`, `wave`, `point`, `present`, `enter`,
  `celebrate`, `sit`, `talk`): decide per clip whether it is keyed in Blender or procedural in code
  (look, idle, flag sway and talk are cheap in code).
- DoD: silhouette test at 24 px; every clip plays on the rest-pose GLB without touching the mesh.

Total for M0–M6: roughly 25–35 working days of focused effort, but the site is publicly usable after
M0 (flat) and impressive after M2 (hero).

## 4. Risks and how the plan absorbs them

| Risk | Mitigation |
|---|---|
| The stylized look drifts (generic low-poly, or too game-like) | M1 locks palette and reference lighting on a dev route before scene work; review screenshots against the chosen hero mockup and DESIGN §2/§3 weekly; README §33's no-HUD rule. |
| World art takes longer than the code | Keep the prop kit tiny (DESIGN §8), reuse it with instancing, use flat backdrops for anything distant, script kits in Blender so changes are re-runs. |
| Scroll-jacking annoys people | Damped progress, skip intro, always-visible menu, flat route one click away. |
| Mobile performance | Tiering decided at M2, not retrofitted; portrait camera authored separately. |
| Content thin for some projects | Non-★ projects live on pedestals with placards only; no empty case studies. |
| Copying references too closely | DESIGN §2 "do not take" and §6 "Not" lists; self-review against WALL-E/EVE/TVA and *Caravan SandWitch* screenshots before each milestone ships. |
| Facts drift | `content.spec.ts` checks every project/timeline entry has a `source` field pointing at PROFILE.md. |

## 5. Immediate next steps

1. Ashish picks a hero mockup and answers the open questions in `PROFILE.md §7` (final yes on "Alu",
   identity order) and DESIGN §4/§12 (headline weight, corner scale).
2. Start **M0**: scaffold + tokens + content model + flat site + Pages fallback.
3. In parallel, build the hero prop kit in Blender (M1).
