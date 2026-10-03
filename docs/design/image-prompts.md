# Image prompts: one per section

> Standalone prompts for ChatGPT image generation, one per section of the site plus four UI states.
> Every prompt is complete on its own: paste it into ChatGPT and generate. Written 2026-10-03; the look
> comes from `docs/DESIGN.md`, the interface from `docs/design/ui-v2.html`.

## How to use

1. Copy one prompt (the whole grey block) into ChatGPT and send it. One prompt per message.
2. **Optional, but it makes results much closer:** attach these with the prompt:
   - `docs/design/logo/logo-ocean.png`: the exact logo
   - `docs/robot/renders/alu_v2_turnaround.png`: Alu from all sides
   - `docs/design/assets/ui-v2-hero.png`: the approved first screen (style + interface)
   - and, where a prompt says so, a photo of the real robot from `public/images/`.
   When you attach them, add this line at the top of the prompt:
   `Use the attached images as exact references for the logo, the robot and the interface.`
3. If one thing comes out wrong, reply with one short fix (see "Fix-up lines" at the end).
4. Save results as `docs/design/mockups/NN-name.png`.

Each prompt has the same five parts: **art style · scene · Alu · interface · text rules**. Only the
scene, Alu's pose and the interface text change between sections.

## The sections at a glance

| # | Section | Where | Alu says (orange word) |
|---|---|---|---|
| 01 | Arrival | glass gate on the cliff top | I wasn't the first thing he **built**. |
| — | Threshold | stepping through the gate | (no message) |
| 02 | Origins | three trails begin | It started with two things at **once**: code and wires. |
| 03 | Robotics | workshop hangar in a cove | This one learned to **walk** on its own. |
| 04 | AI | antenna station on a hill | Some of his machines don't have **bodies**. *(new)* |
| 05 | Software | small harbour village | Some of it runs in **real** kitchens. *(new)* |
| 06 | Crossroads | tomato terraces where the trails meet | This one finds the **ripe** ones. |
| 07 | Record | year markers along the cliff path | Prizes, a paper, and still **counting**. *(new)* |
| 08 | Signal | the same shore at night, contact | Now you know him. Your **turn**. *(new)* |
| + | Scan view · Case study · Menu open · Phone | UI states | |

---

## 01 · Arrival

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the first screen of a personal portfolio website.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; all shadows tinted blue-violet, never black. Low eye-level camera, huge sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone rocks and steps, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts, and old quiet machines slowly being reclaimed by nature. Hopeful and peaceful.

SCENE: A limestone plateau on a cliff top above the sea. In the exact centre stands a tall, thin glass gate: a doorway-shaped glass pane in a slim white frame with softly rounded corners, about four times the robot's height, standing upright on two low, wide limestone steps. The glass reflects the sky, and a soft shaft of warm light falls through it onto the stone. A red-ochre earth path runs from the bottom centre of the image up to the steps. One low-poly pine at the far left edge and one at the far right edge (different shapes, not mirrored). A few faceted white rocks, small grass tufts and dry golden grass. A thin strip of turquoise sea along the horizon; on the right, a faded headland with an old harbour crane. One big faceted white cloud rises behind the gate. The sky (deep blue at the top, pale at the horizon, a soft sun glare in the top-left corner) fills the top half.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he stands right beside the gate at its left base, body angled toward the gate, head turned to the viewer, waving with his outer hand.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above and to the left of his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "I wasn't the first thing he built." Only the word "built" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• Bottom centre: "SCROLL TO FOLLOW" in small, widely spaced grey monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## Threshold (the walk through the gate)

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the transition moment of a personal portfolio website, where the robot guide walks through a glass gate into another world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight; all shadows tinted blue-violet, never black. Calm, cinematic, lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass. Hopeful and peaceful.

SCENE: The camera is low and slightly behind the robot, following him. On a limestone cliff top stands a tall, thin glass gate (a doorway-shaped glass pane in a slim white frame with softly rounded corners) on low limestone steps; it fills about two-thirds of the image height. The glass is clearing from the centre outwards in a soft, expanding ring of light. Through the clear middle we glimpse the land beyond: a bright, sunny grassy clearing where one red-earth trail splits into three. Warm light pours through the gate toward the camera, rim-lighting the robot's edges and casting his long soft shadow back toward the viewer. Turquoise sea and blue sky around the gate.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame), seen from BEHIND and a little to the side as he steps into the gate, one foot lifted mid-step: a big boxy cream-white head with softly chamfered edges, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag swaying and a glowing beacon on top. On his back, a docked power pack: cream housing, orange lid, a small charge meter with three of four bars lit, two metal cells with blue bands, cables to the shoulders. A dark vent with blue slats on the back of his head. Cream shoulder pads, dark upper arms, chunky blue forearms, dark grippers, dark thighs, chunky blue shins, cream boots with orange straps and small heel wheels.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Bottom centre: a small frosted-glass pill with the words "Skip intro" in navy.
No speech bubble and no other labels in this frame.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter). No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 02 · Origins

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "Origins" section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; all shadows tinted blue-violet, never black. Low eye-level camera, huge sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone rocks, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts, and old quiet machines slowly being reclaimed by nature. Hopeful and peaceful.

SCENE: A small grassy clearing on a cliff top in late-morning light. Far behind, a tall thin glass gate in a slim white frame stands small in the distance, glowing faintly. In the foreground one worn red-earth trail splits into three, and all three destinations are visible in the distance like a living map: the LEFT trail drops toward a cove with a weathered pale-teal metal hangar and a yellow crane; the MIDDLE trail climbs a green hill to a white radar dish and a tall antenna mast; the RIGHT trail winds down to a small harbour village of white houses with terracotta roofs by the turquoise sea. Right at the fork stands a waist-high limestone block with two small objects on it, side by side: an old beige computer monitor with a keyboard, and a coil of red and blue wires with a small soldering iron.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he stands at the fork beside the limestone block, one hand resting on it, turned toward the viewer.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "It started with two things at once: code and wires." Only the word "once" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the limestone block: the bold navy title "Class 9" and below it "CODE AND ROBOTICS · SAME YEAR" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (the first navy, the second cyan, the rest pale), followed by "02  ORIGINS" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 03 · Robotics

Optional extra attachments: `public/images/rescue-bot-robot.jpg`, `face-bot-robot.jpg`,
`obstacle-bot-robot.jpg` (add: "Redraw the attached robot photos as low-poly models in this style").

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "Robotics" section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; all shadows tinted blue-violet, never black. Low eye-level camera, big sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone cliffs, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts, and old quiet machines slowly being reclaimed by nature. Hopeful and peaceful.

SCENE: A sheltered cove at the foot of white limestone cliffs, turquoise water at the right. A large weathered corrugated-metal hangar, painted pale teal with soft rust streaks, has its big doors rolled open; inside are workbenches and a hanging engine hoist. An old yellow gantry crane stands beside it, with crates, coiled cables, and pines on the cliff above. A red-earth path runs along the front of the hangar toward the viewer. Along the path, each robot stands on its own low limestone plinth like a museum piece in the open air:
1. Nearest and largest: a 3D-printed four-legged robot dog with 12 joints, white and light-grey printed parts with dark servo joints, caught mid-step.
2. A boxy dark-green rescue vehicle with a row of small wheels along both sides, a small front window, and a small white quadcopter drone parked on its roof.
3. A small flat robot platform on four yellow-and-black omni wheels, with a small camera-sensor module at the front and colourful wires on top.
4. A little four-wheel robot car with yellow wheels, a black deck, and an ultrasonic sensor that looks like two round silver eyes, mounted on a small servo at the front.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he walks along the path toward the robot dog, head turned to look at it, curious.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "This one learned to walk on its own." Only the word "walk" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the robot dog: the bold navy title "JeevI" and below it "12-DOF QUADRUPED · 2025" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (two navy, the third cyan, the rest pale), followed by "03  ROBOTICS" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 04 · AI

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "AI" section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; all shadows tinted blue-violet, never black. Low eye-level camera, huge sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts, and old quiet machines slowly being reclaimed by nature. Hopeful and peaceful.

SCENE: A grassy hilltop high above the sea in clear afternoon light. An old white radar dish on a lattice tower, two small white domed huts, a tall antenna mast with a softly glowing cyan light at its top, a row of solar panels, and thick cables running through the dry grass. The coastline stretches away far below. Along a red-earth path across the hilltop:
1. Nearest: a tall glass slab standing upright in the grass like an outdoor display. On it, a scanned document with rounded cyan boxes highlighting blocks of text (the text is only abstract grey lines, no readable words).
2. A green recycling bin with a small camera on a bendy stalk, looking down at a plastic bottle in front of it.
3. Further back, a long old wooden lab bench under a faded canvas awning, with a row of small screens showing simple line charts, scatter plots and heatmaps in cyan and navy.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he stands beside the glass slab, looking up at it; the cyan boxes reflect softly on his face screen.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "Some of his machines don't have bodies." Only the word "bodies" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the glass slab: the bold navy title "DocLipi" and below it "DOCUMENT AI · 2025" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (three navy, the fourth cyan, the rest pale), followed by "04  AI" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 05 · Software

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "Software" section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Warm late-afternoon sunlight from the left; all shadows tinted blue-violet, never black. Low eye-level camera, big sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts. Hopeful and peaceful.

SCENE: A small working harbour village at the water's edge. Whitewashed stone houses with terracotta roofs and blue shutters, a stone quay with two small wooden fishing boats, an old harbour crane, strings of warm lamps between the houses, pines on the slope behind. Three places in the village are part of the exhibition:
1. A restaurant terrace with a few tables under a striped awning; on its counter a small receipt printer feeds out a long paper receipt, and a tablet shows a live orders board.
2. A small shop front with an open door; on its counter a screen shows an invoice and two small charts.
3. A small clinic building with a red blood-drop sign above the door; through its window, a medical fridge with rows of blood bags, and a desktop screen showing an inventory table.
All screens show simple abstract interface shapes in navy, cream and cyan, with no readable words.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he walks along the quay toward the shop, waving at the restaurant terrace.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "Some of it runs in real kitchens." Only the word "real" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the shop front: the bold navy title "ArthaVidhi" and below it "BILLING FOR SMALL BUSINESSES · 2025" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (four navy, the fifth cyan, the rest pale), followed by "05  SOFTWARE" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 06 · Crossroads

Optional extra attachment: `public/images/tomato-bot-v2.jpg` (add: "Redraw the attached TomatoBot photo as a
low-poly model in this style").

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "Crossroads" section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; all shadows tinted blue-violet, never black. Low eye-level camera, big sky, calm composition with lots of empty space. The world is a sunlit Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts. Hopeful and peaceful.

SCENE: Three red-earth trails arrive from the left, the middle and the right and braid into one path at a terraced tomato farm on a gentle slope above the sea. Low limestone terrace walls, rows of tomato plants on wooden stakes with red and green tomatoes, golden grass at the edges, the turquoise sea and a soft sky behind. Exhibits:
1. Centre, the hero object: a farm robot on a flat black four-wheeled base, carrying a black multi-joint robotic arm with a gripper, a small webcam, and a little round collection bin. The arm reaches for a ripe red tomato on the nearest plant.
2. To the right: a small flower bed with many kinds of flowers, thin soil-moisture sensor stakes, a thin irrigation pipe and a small weatherproof electronics box with a green light.
3. In front, on a limestone plinth: a glass display case holding an open printed research paper, softly lit from inside.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he stands between the farm robot and the glass case, chest up, proud.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "This one finds the ripe ones." Only the word "ripe" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the farm robot: the bold navy title "TomatoBot" and below it "PUBLISHED PAPER · 2026" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (five navy, the sixth cyan, the rest pale), followed by "06  CROSSROADS" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 07 · Record

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the "Record" (timeline) section of a personal portfolio website told as a journey through an illustrated world.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Golden-hour sunlight, low sun near the horizon on the left; long soft shadows tinted blue-violet, never black. Low eye-level camera, big sky, calm composition with lots of empty space. The world is a Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass tufts. Hopeful and peaceful.

SCENE: A red-earth path runs along the edge of a white limestone cliff above a glittering turquoise sea, curving away into the distance. Along the path stands a row of slim, waist-high limestone posts like old survey markers, each with a small brass plate showing one year. From the far distance to the nearest they read "2019", "2021", "2022", "2023", "2024", "2025", "2026". A few posts have a small brass medal hanging from a hook. Pines along the cliff, warm light on everything.

ALU, the robot guide (about 1 m tall; the brightest, roundest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, an orange stripe above the screen, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing beacon on top. Cream torso with a bolted chest plate and three small cyan lights, dark rubber bellows at the neck and waist, a power pack on his back with an orange lid. Cream shoulder pads, dark upper arms, chunky blue forearms with a thin cyan glow ring, dark two-finger grippers. Dark thighs, cream knee pads, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he stands at the nearest post ("2026") in the right foreground, pointing at its plate with one arm and looking back at the viewer.

WEBSITE INTERFACE, drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in navy (#03045E), medium-weight geometric sans-serif.
• Top-right: one solid cream-white (#FFFCF7) pill-shaped capsule with a soft shadow (not see-through), holding left to right: a small navy speaker icon, a small navy sun icon, a thin vertical divider, and a navy pill button containing a white two-line menu icon and the word "Menu" in white.
• Alu's message box, floating above his head: a solid cream-white card with rounded corners and a soft blue-violet shadow. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced navy monospace capitals. Below it, one line of navy text: "Prizes, a paper, and still counting." Only the word "counting" is orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• A small cream rounded card with a soft shadow, linked by a thin navy line ending in a small dot on the 2026 post: the bold navy title "2026" and below it "PAPER PUBLISHED · ENCODEX INTERN" in small grey monospace capitals.
• Bottom-left: a small frosted-glass pill with eight short horizontal dashes in a row (six navy, the seventh cyan, the last pale), followed by "07  RECORD" in small navy monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small capital labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

## 08 · Signal (night, contact)

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): the last section of a personal portfolio website, the contact page, in dark mode: the same illustrated coast at night.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Night lighting: cool moonlight from the upper right plus the robot's own cyan glow; deep blues and navies, NO pure black anywhere. Low eye-level camera, big sky, calm composition with lots of empty space. The world is a Mediterranean sci-fi coast: limestone rocks, low-poly pines, the sea, a small harbour village. Quiet, warm-hearted, peaceful.

SCENE: A deep-blue night sky with a few soft stars and a thin crescent moon. The sea is dark teal with a soft moonlit path on the water. Across the bay, a small harbour village shows a few warm orange lit windows. Far back on the cliff, a tall thin glass gate in a slim white frame glows faintly cyan. In the foreground, on the left half of the image, a flat limestone ledge at the water's edge.

ALU, the robot guide (about 1 m tall; the brightest thing in the frame): a big boxy cream-white head with softly chamfered edges on a small body. The face is a dark navy screen with two big glowing cyan oval eyes (faint horizontal scanlines) and a tiny cyan smile. Four small orange screws at the head's corners, round blue ear disks ringed in orange, a thin metal antenna with a glowing cyan tip on his left side, and at the back right of his head a short mast with a small orange swallowtail flag and a glowing cyan beacon on top. Cream torso with a bolted chest plate and three small glowing cyan lights, a power pack on his back with an orange lid. Chunky blue forearms with a glowing cyan ring, dark grippers, chunky blue shins, cream boots with orange straps, small heel wheels.
Pose: he sits on the limestone ledge, legs dangling over the water, facing the sea with his head turned to the viewer. His eyes, chest lights, antenna tip and beacon glow cyan and softly light the rock around him.

WEBSITE INTERFACE (night version), drawn flat and razor-sharp on top of the 3D scene like a real website screenshot:
• Top-left: the logo, a small ocean-blue (#0077B6) circle containing a thin cream line-drawn geometric monogram made of straight strokes (two upright lines, a crossbar, two diagonals) with one short orange bar at its top right like a tiny flag, followed by the name "Ashish Gupta" in near-white, medium-weight geometric sans-serif.
• Top-right: one pill-shaped capsule in translucent deep navy with a thin light outline, holding left to right: a small white speaker icon, a small white moon icon, a thin vertical divider, and a white pill button containing a navy two-line menu icon and the word "Menu" in navy.
• The right third of the screen: a solid deep-navy (#0A1070) panel with large rounded corners. Inside, a large white heading "Say hello". Below it, four lines in small monospace (labels in pale blue, values in white): "EMAIL   haitomns@gmail.com", "PHONE   +977 980 920 4764", "GITHUB   haitomnsg", "LINKEDIN   haitomnsg". Below those, a minimal form: two input fields with thin light outlines labelled "Your name" and "Message", and a cyan (#00B4D8) pill button "Send".
• Alu's message box, floating above his head (night style): a solid deep-navy card with rounded corners and a thin cyan outline. Inside, a small header row: a tiny navy rounded-square badge showing two glowing cyan oval eyes and a small smile, then the word "ALU" in small, widely spaced white monospace capitals. Below it, one line of white text: "Now you know him. Your turn." Only the word "turn" is soft orange. A short, smoothly curved tail on the bottom edge points down at Alu's head.
• Bottom-left: a small dark frosted-glass pill with eight short horizontal dashes in a row (seven pale white, the last cyan), followed by "08  SIGNAL" in small white monospace capitals.

TEXT RULES: Spell every word and number exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and a monospace for the small labels. No other text anywhere, no extra logos, no watermark or signature, no game interface.
```

---

## UI states (extra)

### Scan view (focus on a project)

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): a portfolio website in "scan view", where focusing on a project shows its engineering details.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render. Simple faceted shapes, flat matte colours, no textures, no shine. Calm composition, lots of empty space.

SCENE: Terraced tomato farm on a gentle slope above a turquoise sea: limestone terrace walls, rows of tomato plants on stakes with red and green tomatoes, three red-earth trails joining into one. In the centre, a farm robot on a flat black four-wheeled base with a black multi-joint robotic arm and gripper, a small webcam and a little round collection bin, reaching for a ripe tomato. The whole world is tinted slightly teal and a little desaturated, as if seen through a scanner. The farm robot alone is outlined with a thin glowing cyan line.
Four thin straight navy leader lines (horizontal or at 45 degrees) run from parts of the robot to four small cream label chips with navy monospace capitals; each line ends on the robot in a small cyan dot:
- from the arm: "6-DOF ARM · INVERSE KINEMATICS"
- from the webcam: "YOLOv11 · 88% RIPENESS"
- from the base: "U-NET PATH SEGMENTATION"
- from the electronics: "RASPBERRY PI"
A small cream-and-blue robot with a big boxy head, a dark face screen with two glowing cyan oval eyes and a small orange flag on his head stands a little aside, his eyes glowing brighter.

WEBSITE INTERFACE, flat and razor-sharp on top:
• Top-left: a small ocean-blue circle logo with a thin cream line-drawn geometric monogram and one short orange bar at its top right, then "Ashish Gupta" in navy.
• Top-right: one solid cream pill-shaped capsule holding a navy speaker icon, a navy sun icon, a thin divider, and a navy pill button with a white two-line icon and the word "Menu".
• Bottom-left: a small frosted pill with eight short dashes (five navy, the sixth cyan, the rest pale) and "06  CROSSROADS" in navy monospace capitals.
• Bottom centre: a small frosted pill "Click to open".

TEXT RULES: Spell every word exactly as written in quotes above. No other text, no speech bubble, no watermark.
```

### Case study open

Optional extra attachment: `public/images/tomato-bot-v2.jpg` (add: "Use the attached photo as the photo
inside the panel").

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): a portfolio website with a project case study open.

BACKGROUND: A stylized low-poly 3D scene (flat matte colours, faceted shapes): a terraced tomato farm on a slope above a turquoise sea, softly defocused with haze and dimmed by about 40%. On the left of the dim scene, a small glass gate in a slim white frame stands open, and beside it a small cream-and-blue robot with a big boxy head, two glowing cyan oval eyes and a little orange flag stands idle.

PANEL: From the right edge, a solid cream-white (#FFFCF7) panel covers about 37% of the width, full height with a small margin, with large rounded corners and a soft shadow. At its top right, a small frosted chip "Esc · Close". Inside, left-aligned with generous spacing, top to bottom:
- small grey monospace capitals "ROBOTICS · AI · SOFTWARE"
- a large bold navy (#03045E) title "TomatoBot"
- one line of navy text: "A robot that finds ripe tomatoes and picks them."
- a wide photo with rounded corners of a real small farm robot (black four-wheeled base, black robotic arm, webcam) on green grass
- a row of three small rounded thumbnail images
- a navy heading "What I built" followed by three lines of soft grey placeholder text
- one line of small navy monospace capitals: "YOLOv11 · U-NET · RASPBERRY PI · ANDROID"

INTERFACE: Top-left a small ocean-blue circle logo with a thin cream line-drawn geometric monogram and one short orange bar, then "Ashish Gupta" in navy. Top-right one solid cream pill-shaped capsule holding a navy speaker icon, a navy sun icon, a thin divider and a navy pill button with a white two-line icon and the word "Menu".

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and monospace for small labels. No other text, no speech bubble, no watermark.
```

### Menu open

```text
Create a website mockup screenshot, landscape 3:2 (1536×1024): a portfolio website with its menu open.

BACKGROUND: A stylized low-poly 3D scene (flat matte colours, faceted shapes, soft warm light): a limestone cliff top above a turquoise sea, a tall thin glass gate in a slim white frame in the centre, a small cream-and-blue robot with a big boxy head and glowing cyan eyes beside it, pines at the edges, a big faceted cloud. The scene is softly blurred and dimmed.

PANEL: From the right, a solid cream-white (#FFFCF7) panel covers about 40% of the width, full height with a small margin, with large rounded corners and a soft shadow. Inside, a vertical list of eight items separated by thin hairlines; each item is a small grey monospace number followed by a large navy (#03045E) name: "01 Arrival", "02 Origins", "03 Robotics", "04 AI", "05 Software", "06 Crossroads", "07 Record", "08 Signal". A small cyan dot sits before "Arrival" to show the current place. Under the list, a row of three small outlined pill buttons: "Read as a page", "Day / Night", "Sound off". At the bottom of the panel, three small grey monospace lines: "EMAIL", "GITHUB", "LINKEDIN".

INTERFACE: Top-left a small ocean-blue circle logo with a thin cream line-drawn geometric monogram and one short orange bar, then "Ashish Gupta" in navy. Top-right one solid cream pill-shaped capsule holding a navy speaker icon, a navy sun icon, a thin divider and a navy pill button with a white X icon and the word "Close".

TEXT RULES: Spell every word exactly as written in quotes above. Clean geometric sans-serif (like Geist or Inter) and monospace for the small numbers and labels. No other text, no speech bubble, no watermark.
```

### Phone (hero, portrait)

```text
Create a mobile website mockup screenshot, portrait 2:3 (1024×1536): the first screen of a personal portfolio website on a phone.

ART STYLE: Stylized low-poly 3D illustration, like a polished Blender render or a premium indie-game still. Simple faceted shapes, flat matte colours, no textures, no glossy shine. Soft warm sunlight from the upper left; shadows tinted blue-violet, never black. Calm, lots of empty sky. A sunlit Mediterranean sci-fi coast: warm-white limestone, dark-green low-poly pines, a turquoise sea, red-ochre earth paths, dry golden grass.

SCENE: A tall glass gate (a doorway-shaped glass pane in a slim white frame with softly rounded corners) stands in the centre of the lower half on low limestone steps, with a red-earth path running down to the bottom edge. One low-poly pine at the left edge, a strip of turquoise sea at the horizon with a faded headland and an old crane, one big faceted white cloud behind the gate. The sky fills the top third.

ALU, the robot guide (about a quarter of the gate's height): a big boxy cream-white head with chamfered edges, a dark navy face screen with two big glowing cyan oval eyes and a tiny smile, orange screws, blue ear disks, an antenna with a glowing tip on his left side, a small orange swallowtail flag on a short mast at the back right of his head; cream torso with a chest plate and three cyan lights, blue forearms and shins, dark joints, cream boots with orange straps. Pose: standing at the gate's left base, waving, head turned to the viewer.

WEBSITE INTERFACE, sized for a phone, flat and razor-sharp:
• Top-left: a small ocean-blue circle logo with a thin cream line-drawn geometric monogram and one short orange bar at its top right, then "Ashish Gupta" in navy.
• Top-right: only a round navy button with a white two-line menu icon.
• Above Alu: his message box, a cream rounded card with a soft shadow, a header row with a tiny navy badge showing two cyan eyes and "ALU" in spaced monospace capitals, then two lines of navy text: "I wasn't the first thing he built." with only "built" in orange, and a short curved tail pointing at his head.
• Bottom centre: "SCROLL TO FOLLOW" in small, widely spaced grey monospace capitals.

TEXT RULES: Spell every word exactly as written in quotes above. No other text, no extra logos, no watermark.
```

---

## Fix-up lines (send one at a time, after a result)

- **Logo wrong:** `Keep everything else exactly the same. Fix only the logo top-left: a small ocean-blue circle with a thin cream line monogram made of straight strokes and one short orange bar at its top right, followed by "Ashish Gupta" in navy.` (Works best with `logo-ocean.png` attached.)
- **Menu wrong:** `Keep everything else. The top-right control must be one solid cream capsule (not see-through) holding a navy speaker icon, a navy sun icon, a thin divider and a navy pill with a white two-line icon and the word "Menu".`
- **Message box wrong:** `Keep everything else. Redraw Alu's message box: a solid cream card with rounded corners and a soft shadow, a header row with a tiny navy badge showing two cyan eyes and the word ALU in spaced monospace capitals, one line of navy text with only one orange word, and a short curved tail pointing at Alu's head.`
- **Text misspelled:** `Keep everything else. Fix the text so it reads exactly: "…"`
- **Alu changed:** `Keep everything else. Fix the robot: [name the part, e.g. two big oval eyes, not round; the orange flag at the back right of his head; blue forearms and shins].` (Attach `alu_v2_turnaround.png`.)
- **Too busy:** `Same scene with half as many props and more empty sky. Keep the robot, the main exhibit and the interface.`
- **Too realistic or glossy:** `Make it flatter: matte flat colours, simple faceted low-poly shapes, no textures, no shine.`

## Notes

- Check every result's text before using it, especially the phone number and the small labels.
- Placard and scan-label facts come from `docs/PROFILE.md` only.
- Proposals still to confirm: the logo colourway (Ocean recommended), the four *new* Alu lines and
  the eight-chapter numbering. After that, DESIGN.md §5, §8, §9, §10 and §14 get updated.
