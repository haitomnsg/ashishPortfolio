# Interactive 3D Portfolio — Design & Build Reference

> **Purpose:** This README is the source of truth for building my personal portfolio website. It captures the vision, storytelling, visual direction, robot mascot, interaction philosophy, and content structure I have described. It is **not a project-management plan or task list**. Use it as the design/build context while making implementation decisions.

> **Direction update (2026-10-03):** The look moved from a clean, white, Apple-like exhibition to a **stylized, sunlit sci-fi coast** inspired by the art direction of the game *Caravan SandWitch*. The world is built from a few simple, faceted shapes with flat matte colours. The robot was redesigned to match (Alu v2). The story, structure and principles are unchanged. The sections that changed are 1, 2, 3, 4, 9, 15–18, 20, 23, 27, 31–33, 38 and 39. `docs/DESIGN.md` holds the concrete specs.

---

## 1. Core Vision

I do not want a conventional portfolio website that looks like a résumé placed on a webpage.

The portfolio should feel like an **interactive cinematic experience** where the visitor enters a small world and is guided through my work by a robot character.

The website should communicate that I am a:

- Robotics Engineer
- Software Engineer
- AI Engineer

The experience should show **what I have built, how I think, what I have worked on, and how my interests connect**, rather than simply presenting a list of technologies or résumé sections.

The overall feeling should be:

- Premium
- Minimal
- Cinematic
- Futuristic
- Personal
- Curious
- Technically sophisticated
- Award-style / showcase-quality
- Warm and natural, like a real place, not a sterile void
- Calm and uncluttered: a few simple shapes rather than visual noise

The site should feel like a **digital experience**, not a collection of cards.

---

# 2. The Main Story

The visitor should feel as if they are entering my world.

The opening concept is approximately:

1. Open on a calm, sunlit coast: a white limestone plateau, a strip of sea, a huge sky. Almost no UI.
2. A tall glass gateway stands in the center of the scene.
3. The robot mascot stands right beside it and turns to look at the visitor.
4. Light comes through the gateway.
5. The robot says one short line (see §9) and invites the visitor to follow.
6. The robot walks through the entrance.
7. The world behind/through the entrance becomes the portfolio environment.
8. The visitor is then taken through my story, projects, engineering work, and experiences.

The portal should not feel like a normal website navigation menu disguised as a door. It should feel like an actual transition from the **landing page into another world**.

The inspiration is the feeling of a futuristic doorway/portal such as the TVA-style idea from *Loki*: an architectural entrance that represents access to another place/world. Do not copy the actual TVA design. The goal is the **concept of a mysterious gateway to another world**.

The portal can be:

- Glass-like
- Architectural
- Minimal
- Futuristic
- Brightly illuminated
- Slightly mysterious
- Integrated naturally into the environment
- Standing on its own in a natural landscape, like a glass pane on a cliff top

The opening should be visually understandable even without text.

---

# 3. The Robot Mascot

The robot is one of the most important elements of the entire website.

It is not just decoration.

It is the **narrator / guide / visual identity of the portfolio**.

The visitor should recognize the robot as the character that represents me and guides them through the website.

## Character direction

The robot should have the emotional appeal of a cute, friendly, compact exploration robot.

The inspiration includes the emotional/industrial friendliness of WALL-E-like robots, but the final character must be **original and unique**, not a copy of WALL-E.

The robot should feel:

- Cute
- Friendly
- Curious
- Intelligent
- Small compared with its environment
- Technological
- Slightly mechanical
- Expressive through body movement
- Premium rather than toy-like

It should work as a real 3D model that can later be animated.

It should be modelled in the same stylized style as the world: simple faceted shapes, flat matte colours, no glossy plastic.

## Color direction

The primary visual identity of the robot is:

- Warm cream-white shell (sun-faded, not pure white)
- Power/sky blue limbs and details
- Dark navy-plum joints, soles and face screen for contrast
- Small orange details: screws, straps, wheel hubs, the flag
- Soft cyan glow on everything that is "on": eyes, status lights, antenna tip, beacon
- Painted grey metal for small mechanical parts

The robot should primarily read as a **cream-white + power-blue robot**, with orange only as a small accent.

The blue should feel clean and futuristic rather than neon/cyberpunk.

Avoid making the robot entirely blue.

White should remain a major part of the body.

## Current design (Alu v2, 2026-10-03)

The robot's working name is **Alu**. The current model is a stylized low-poly explorer robot built to match the world:

- A big boxy head with a dark screen face: two large glowing eyes with scanlines and a small smile
- Blue ear disks, an antenna with a glowing tip, a carry handle, and a small swallowtail flag on a short mast with a beacon
- A bolted chest plate with status lights, a docked power pack on the back, and cables to the shoulders
- Rubber bellows at the neck and waist, servo caps at the joints, pistons on the legs
- Chunky blue forearms and shins, cream boots with orange straps, and small heel wheels

Files: `docs/robot/alu_v2_build.py` (rebuild script), `docs/robot/alu_v2.blend`, `public/models/alu.glb` (web model), and renders in `docs/robot/renders/`.

## Important physical characteristics

The robot should be designed with 3D modeling and animation in mind.

It should have:

- A recognizable silhouette
- A compact body
- Clearly separated mechanical components
- Articulated arms
- A head/sensor area capable of expressive movement
- Wheels and/or compact locomotion elements
- Simple joints that can be rigged
- A body that can turn toward things
- A design that supports walking/driving/turning/looking animations
- Enough mechanical detail to look interesting in close-up
- Not so much detail that it becomes difficult to model or animate

The character should be recognizable even as a small object on screen.

## Character personality

The robot should communicate personality through animation rather than dialogue-heavy exposition.

It may speak, but only in very short lines shown in a speech bubble, one line at a time and at most one per chapter. It never holds a conversation.

Useful behaviors include:

- Looking around
- Looking toward the visitor/camera
- Looking toward a project
- Pausing and observing
- Small head movements
- Curious reactions
- Gentle waving
- Pointing
- Walking/driving
- Turning around
- Looking back before entering a portal
- Celebratory movement after completing something
- Sitting/pausing in an environment
- Exploring a new scene

Animations should be subtle and believable.

Avoid exaggerated cartoon animation.

---

# 4. Visual Identity

The overall visual language is a **warm, natural world with a cool, precise robot and interface inside it**.

### World colors

- Warm white limestone
- Sky blue
- Muted turquoise sea
- Olive / pine green
- Red-ochre earth
- Dry-grass peach

### Identity colors

- Cream-white + power blue (the robot)
- Cyan glow for anything that is powered on
- Orange as a small accent
- Deep navy for text and interface

Shadows are soft blue-violet, never black.

The website should not become a generic "blue tech website."

Blue is the identity color of the robot and the technology, set inside a warm, natural world.

## Light mode

Light mode is **daytime on the coast**:

- Warm sunlight and a huge blue sky
- Soft blue-violet shadows
- Light atmospheric haze
- The glass gateway reflecting the sky
- Simple, faceted 3D shapes
- Minimal UI

## Dark mode

Dark mode is **night on the same coast**:

- Deep blue night sky (not black)
- A few warm lights in the world
- The robot's cyan glow and the machines' lights carry the scene
- White typography
- Stronger contrast
- Cinematic atmosphere

The two modes should feel like the **same world under different lighting conditions**, not two unrelated designs.

---

# 5. Design Philosophy

The website should prioritize **experience over UI density**.

Avoid:

- Large grids of generic project cards everywhere
- Excessive buttons
- Excessive text
- Generic glassmorphism
- Random floating 3D objects
- Huge gradients
- Cyberpunk aesthetics
- Excessive neon
- Typical developer portfolio templates
- "Skill percentage" meters
- Generic résumé layouts
- Overuse of badges
- Every section looking like a separate landing page

Instead, use:

- Spatial storytelling
- 3D environments
- Camera movement
- The robot
- Lighting
- Architectural transitions
- Environmental changes
- Scroll-driven interactions
- Subtle UI
- Typography
- Carefully timed animation
- Meaningful motion

The interface should become visible when useful and disappear when it is not.

---

# 6. Portfolio Structure

The portfolio should tell a story rather than simply divide everything into conventional sections.

A rough conceptual progression is:

**Arrival → Introduction → Exploration → Work → Engineering → Projects → Story → Contact**

However, do not interpret this as a rigid page structure.

The website can use:

- Rooms
- Paths
- Corridors
- Open landscapes
- Portals
- Platforms
- Abstract environments
- Project-specific scenes
- Transitions between worlds

The portfolio should **not be limited to rooms**.

Initially, rooms were considered for:

- AI
- AI/ML Engineering
- Software Engineering

But the realization is that rooms alone are too restrictive for everything I want to show.

Therefore, the final experience should use a mixture of spatial metaphors.

For example:

- A path can represent progression.
- A large open environment can represent exploration.
- A portal can represent moving between areas.
- A project can have its own small environment.
- A timeline can exist physically in the environment.
- A group of projects can appear along a road/path.
- A major project can become a larger interactive scene.

The robot can move through these spaces.

---

# 7. My Story Must Not Be Presented as a Linear Career Progression

An important constraint:

Do **not** create a story implying:

> Software → AI/ML → Robotics

That would be inaccurate.

Programming and robotics both started around **Class 9**.

The story should communicate that these interests developed alongside one another.

A useful conceptual model is a **converging set of paths** rather than a single staircase.

For example:

- Programming path
- Robotics path
- AI/ML path

These paths can intersect and eventually become one combined engineering identity.

The website should communicate that software, AI, and robotics are interconnected parts of my work.

---

# 8. Personal Timeline / Background

The portfolio should be able to communicate the following background:

- I started programming around Class 9.
- I have been building things since then.
- Robotics also started around Class 9.
- I have a Diploma in Computer Engineering.
- The diploma period can be represented as an important software/computer-engineering phase.
- I have studied and built AI/ML projects.
- I have continued developing across software, AI, and robotics.
- These areas should not be presented as completely separate careers.

The exact storytelling can be creative, but the facts should remain accurate.

The portfolio should feel like:

> "This is how I became someone who builds systems across software, AI, and robotics."

rather than:

> "Here are three unrelated skill categories."

---

# 9. Introduction / Identity Reveal

The website should introduce who I am, but the identity reveal can be designed creatively.

I do not necessarily want the first screen to immediately dump:

> "Hi, I am X, Robotics Engineer..."

The experience can first create curiosity.

For example:

- The visitor enters the world.
- The robot guides them.
- The environment starts revealing information.
- My identity becomes clearer as the journey progresses.

The current decision for the first screen:

- **No headline.** The robot speaks one short line in a speech bubble, for example: *"I wasn't the first thing he built."*
- The robot **never says my name**. My name appears only as a small wordmark in the corner.
- As the visitor scrolls, the robot continues the story in short, abstract lines. Each line hints at something real; nothing is invented.
- All text stays minimal.

However, the visitor should not be confused about what the website represents.

There should be a balance between:

**mystery + clarity**

The experience should eventually make it obvious:

- Who I am
- What I do
- What I build
- What technologies/fields I work with
- What projects I have created

---

# 10. Project Presentation

Projects should not simply be:

```text
Project Name
Description
Tech Stack
GitHub button
```

inside a repetitive card grid.

Projects should feel like **artifacts discovered inside the world**.

Possible representations:

- Robot approaches a project station.
- Project appears as a 3D object.
- A project environment opens.
- A holographic visualization appears.
- The camera transitions into a project-specific scene.
- A physical object represents the project.
- A path contains multiple project "stops."
- A project can be expanded into a detailed case study.

The goal is to make the visitor remember the projects as experiences.

## Project information should still be accessible

The visual experience must not sacrifice useful information.

A project should be able to communicate:

- What problem it solves
- What I built
- My role
- Technologies used
- Architecture where relevant
- Important technical decisions
- Challenges
- Results/outcomes where available
- Images/videos/demos
- GitHub/live demo where available

But this information should appear progressively rather than all at once.

---

# 11. Engineering Domains

The portfolio needs to represent the intersection of:

## Robotics

Possible content:

- Robotic systems
- Robot control
- Computer vision
- Embedded systems
- Hardware/software integration
- Automation
- Physical prototypes
- Robotics experiments

## Artificial Intelligence / Machine Learning

Possible content:

- AI systems
- Machine learning
- Computer vision
- Deep learning
- AI automation
- Model development
- Intelligent applications

## Software Engineering

Possible content:

- Full-stack applications
- Backend systems
- APIs
- Automation
- Developer tools
- Architecture
- Production systems
- Web applications

These should feel interconnected.

A robotics project can involve AI and software.

An AI project can involve software engineering.

A software project can involve automation.

Do not force every project into exactly one category.

---

# 12. Navigation Philosophy

Navigation should not feel like a traditional navbar controlling every part of the site.

The primary navigation can be spatial.

The robot can act as the user's guide.

Potential navigation mechanisms:

- Scroll
- Mouse movement
- Camera movement
- Clicking environmental objects
- Portal interactions
- Robot movement
- Small minimal navigation overlay
- A subtle world map / progress indicator

There can still be a conventional fallback navigation for usability and accessibility.

The visitor should never become trapped in an animation.

There must always be a clear way to:

- Move forward
- Go back
- Open a project
- Return home
- Access contact/about information

---

# 13. Camera & Motion

Motion is a core part of the design.

Animations should feel cinematic rather than like UI effects.

Important principles:

- Smooth transitions
- Natural easing
- Inertia
- Depth
- Parallax
- Environmental movement
- Camera choreography
- Subtle character animation

Avoid:

- Constant spinning
- Excessive zooming
- Aggressive camera shake
- Motion everywhere simultaneously
- Long animations that block navigation

The camera should sometimes behave like a film camera.

The robot should remain a physical object in the scene.

---

# 14. Scroll Experience

Scroll should ideally control the journey rather than simply move vertically through flat sections.

For example:

- Scroll forward → robot moves forward
- Environment changes
- Camera moves
- Portal opens
- Project appears
- Robot interacts with object
- Scene transitions

But this must remain usable.

If the user scrolls quickly, the system should handle it gracefully.

Avoid forcing users to watch long animations before they can continue.

The website should support:

- Desktop mouse
- Trackpad
- Touch devices where practical
- Reduced-motion preferences

---

# 15. 3D Environment Direction

The world is a **stylized, sunlit sci-fi coast**, inspired by the art direction of *Caravan SandWitch*: a Provence-like place where old machines are slowly being reclaimed by nature. It should feel natural and real, without being photorealistic.

The environment should be minimal enough that the robot remains the focus.

Environment qualities:

- Warm white limestone plateaus and cliffs
- A strip of turquoise sea and a huge open sky with sculpted clouds
- A few pines, dry grass and red-ochre paths
- Old machines living in nature (cranes, antennas, containers): quiet and hopeful, never menacing
- Warm sunlight, soft blue-violet shadows, light haze
- Light beams through the glass gateway
- Depth
- Large negative space

Style rules (these keep it buildable in 3D):

- Simple low-poly shapes with hard, faceted edges
- Flat matte colors, almost no textures
- Few props, reused across scenes; every object should be buildable from a few simple shapes
- Distant elements (sky, headlands) can be flat backdrops

The art style comes from a game, but the website must not behave like a game level: no HUD, no quest markers, no collectibles.

It should feel like a **calm, explorable diorama**: an exhibition built around one person, set outdoors.

---

# 16. Portal / Gateway Design

The gateway is a major visual motif.

It should look like an entrance to another world.

Desired characteristics:

- A tall, thin glass pane with softly rounded corners in a slim white frame
- Standing upright in the landscape, in the center of the opening scene, with the robot right beside it
- The glass reflects the sky
- Cool light coming through it, with a gentle shaft of light on the ground in front
- Natural environment visible through it when appropriate
- Strong depth
- Slight atmospheric haze

The gateway can represent:

- Entering the portfolio
- Entering a major project
- Changing chapters
- Moving from one engineering domain to another
- Opening a deeper case study

It should become a reusable visual language throughout the website.

---

# 17. Lighting

Lighting is extremely important.

The lighting should create the premium cinematic quality.

Use concepts such as:

- Warm sunlight as the key light
- Blue-violet sky light filling the shadows
- Rim lighting
- Cyan emissive accents on things that are powered on
- Light shafts through the gateway
- Subtle bloom, only on things that glow
- Soft shadows
- Ambient occlusion where appropriate
- Reflections only on the gateway's glass
- Atmospheric haze

The robot should be readable even in dark environments.

Blue emissive elements should be subtle.

Avoid excessive bloom.

---

# 18. Materials

Materials should be simple and matte, so the world looks hand-crafted rather than rendered.

Preferred materials:

- Flat matte colors (a painted look)
- Warm white stone
- Matte painted metal
- Dark rubber
- Cloth (the robot's flag)
- Glass, only for the gateway
- Soft emissive cyan for powered parts

Avoid glossy plastic, chrome and heavy textures.

The world should feel tactile.

---

# 19. Typography

Typography should be:

- Modern
- Clean
- Highly readable
- Premium
- Minimal

Use one strong primary typeface throughout the system, with limited supporting typography if necessary.

Typography should support both:

- Large cinematic headlines
- Dense technical information

Do not use overly futuristic fonts that sacrifice readability.

---

# 20. UI System

The UI should be intentionally minimal.

Possible UI elements:

- Small navigation controls
- Project metadata
- Tiny labels
- Progress indicator
- Chapter name
- Scroll hint
- Contact action
- Theme toggle
- Accessibility controls
- The robot's speech bubble: a white rounded bubble with a small cyan name tag and one highlighted word

UI should feel integrated with the environment.

The interface is **cool and precise** (navy text, cyan accents, frosted glass for small controls, solid panels for anything you read). It sits on top of the warm world, the same contrast the game uses.

Avoid floating dashboard-style UI everywhere.

Avoid game-style UI: health bars, minimaps, quest markers, inventories.

The website should remain primarily spatial and visual.

---

# 21. Responsive Design

The desktop experience is the main showcase because the 3D experience needs enough screen space.

However, mobile must still be treated as a first-class experience.

On smaller screens:

- Simplify scenes where necessary.
- Reduce 3D complexity.
- Reduce particle counts.
- Reduce animation complexity.
- Preserve the robot as the main character.
- Keep the storytelling intact.
- Ensure text remains readable.
- Do not simply shrink the desktop scene.

A mobile visitor should still understand the story.

---

# 22. Performance Philosophy

The website can be technically ambitious, but performance is important.

The experience should avoid unnecessary heavy rendering.

Consider:

- Lazy-loading 3D assets
- Progressive asset loading
- Optimized GLB/GLTF models
- Texture compression
- Lower-resolution textures when appropriate
- LODs
- Frustum culling
- Efficient particle systems
- Instancing where useful
- Lazy-loading project scenes
- Avoiding unnecessarily large textures
- GPU-friendly shaders
- Mobile-specific quality settings

The initial screen should load quickly enough to establish the experience.

The visitor should not stare at an empty screen while the entire portfolio downloads.

---

# 23. 3D Model / Asset Workflow

The robot is modeled separately in Blender and imported into the website. The current model is `public/models/alu.glb` (Alu v2, exported in a neutral rest pose).

The website should be designed around a standard web-friendly 3D workflow:

- GLB / GLTF
- Flat vertex colors on a few matte materials (the stylized look needs almost no texture maps)
- Low triangle counts (Alu v2 is about 8k triangles)
- Rigged model where animation is required (Alu uses named pivot joints)
- Separate animations where useful

The robot model should be prepared so it can support:

- Idle
- Walk / move
- Turn
- Look
- Wave
- Point
- Enter portal
- React
- Stop
- Interaction animations

The website should not depend on baked video for the core robot experience.

The robot should remain a real interactive 3D asset.

---

# 24. Suggested Technical Direction

The implementation can use a modern web 3D stack.

A likely direction is:

- React
- Three.js
- React Three Fiber
- Drei where useful
- GSAP and/or another robust animation system
- WebGL
- GLB/GLTF assets

The exact technology can change if a better technical choice exists, but the final implementation should preserve the intended experience.

The codebase should be maintainable.

3D logic, UI, animation state, content, and assets should not become one giant component.

---

# 25. Interaction With the Robot

The robot should react to the user's presence.

Examples:

### Mouse movement

The robot can subtly:

- Look toward the cursor
- Turn its head
- Shift attention toward interactive objects

### Hover

When hovering an interactive object:

- Robot notices it
- Object subtly reacts
- Small lighting change
- Minimal contextual label can appear

### Click

A click can trigger:

- Robot walking toward an object
- Portal opening
- Camera transition
- Project environment
- Case-study interface

### Scroll

The robot can physically move as the visitor progresses.

The visitor should feel that the robot is part of the same physical world.

---

# 26. The Robot Should Not Become Annoying

The mascot is important, but it must not dominate every second.

Avoid:

- Constant talking
- Constant waving
- Blocking content
- Following the cursor aggressively
- Repeating animations
- Making the visitor wait for the robot

The robot should feel alive but respectful.

It should sometimes simply exist in the environment.

---

# 27. Sound

Sound can enhance the experience but must never be required.

Potential sounds:

- Very subtle mechanical movement
- Footstep/wheel sounds
- Portal activation
- Soft environmental ambience (wind, distant sea)
- UI interaction sounds
- Gentle futuristic atmosphere

Audio should:

- Start muted by default if appropriate.
- Provide a clear sound control.
- Never surprise the visitor with loud audio.
- Respect browser autoplay restrictions.
- Respect reduced-motion/accessibility expectations where relevant.

---

# 28. Accessibility

Despite the cinematic design, the website must remain usable.

Include:

- Keyboard navigation where possible
- Accessible buttons
- Semantic HTML
- Good color contrast
- Screen-reader-friendly important information
- Reduced-motion support
- Fallback content for major 3D sections
- Accessible project descriptions
- A way to skip long animations
- A conventional way to access important content

The 3D experience should enhance the content, not become the only way to access it.

---

# 29. Content Hierarchy

The visitor should eventually understand:

### Who I am

A robotics + software + AI engineer who builds systems and experiments across these fields.

### What I build

Real projects, software, AI systems, robotics systems, experiments, and technical products.

### How I think

Through engineering decisions, experimentation, problem solving, and building.

### What I have done

Projects, work, education, experiments, achievements, and technical experiences.

### Where to find me

Relevant contact and professional links.

---

# 30. Portfolio Storytelling Style

The storytelling should be written in first person where appropriate.

The tone should be:

- Confident
- Curious
- Technical
- Human
- Concise
- Not corporate
- Not overly dramatic
- Not full of buzzwords

Avoid writing like:

> "We leverage cutting-edge technologies to revolutionize..."

Prefer language like:

> "I build systems where software, intelligence, and machines meet."

The website should feel like a real engineer showing their work.

---

# 31. The Website Should Feel Like an Exhibition

A useful mental model:

> Imagine an engineering exhibition designed specifically around one person, set outdoors in a calm, stylized world.

The visitor walks through it.

The robot is the guide.

The projects are artifacts.

The environments represent chapters.

The portals represent transitions.

The timeline represents the journey.

The UI provides information when needed.

The entire experience is the portfolio.

---

# 32. Visual References / Inspiration Principles

The visual direction can take inspiration from:

- **The art direction of *Caravan SandWitch*** (Studio Plane Toast; art director Charles Boury), the main reference for the look: stylized low-poly shapes, a world inspired by a real place, hopeful sci-fi, bright round characters against calmer backgrounds, and a cool interface over a warm world
- Glass gateways standing in natural landscapes (`inspo/Glass_One.jpg`, `inspo/Glass_Two.jpg`)
- Apple-like restraint in the interface
- High-end cinematic camera work
- Interactive digital exhibitions
- Friendly robotics

But the final site should not look like a clone of another website. Do not copy the game's characters, van, locations, logo or UI.

The goal is to combine these references into a distinct identity.

---

# 33. What the Design Must Avoid

Do not turn the portfolio into:

- A normal résumé website
- A generic developer portfolio template
- A collection of Tailwind cards
- A cyberpunk website
- A gaming website: the art style is game-inspired, but there are no HUDs, health bars, minimaps, quest markers, inventories or game menus
- A copy of *Caravan SandWitch*
- A photorealistic or glossy 3D render
- A dashboard
- A 3D demo with no meaningful content
- A collection of random 3D objects
- A purely decorative animation
- A linear slideshow
- A room-only portfolio
- A software → AI → robotics career story

The 3D should have meaning.

---

# 34. Core Experience Principle

Every major visual element should answer at least one of these questions:

**Why is this here?**

**What part of my story does this represent?**

**What does this tell the visitor about what I build?**

**Does this make the portfolio more memorable?**

If an effect exists only because it looks technically impressive, it should be reconsidered.

---

# 35. Desired Emotional Journey

The visitor should ideally experience something like:

**Curiosity**

"What is this?"

↓

**Recognition**

"Oh, this is a portfolio."

↓

**Connection**

"This little robot is guiding me."

↓

**Exploration**

"There is an actual world here."

↓

**Discovery**

"This person has built all these things."

↓

**Understanding**

"I can see how software, AI, and robotics connect."

↓

**Interest**

"I want to inspect this project."

↓

**Memory**

"I remember the robot and the experience."

The portfolio should be memorable because of the combination of **story + engineering + visual experience**.

---

# 36. Important Design Constraint

The website must remain a portfolio first.

The experience should never become so elaborate that visitors cannot quickly access the actual work.

There should always be a path from:

**visual experience → actual project information**

The cinematic layer is the presentation.

The projects and engineering work are the substance.

---

# 37. Final Creative Direction

The final website should feel like:

> **A small robot opening a door into the world of an engineer.**

The visitor does not simply scroll through a résumé.

They enter.

They explore.

They follow the robot.

They encounter things I have built.

They see the evolution of my interests.

They move through software, AI, robotics, and the intersections between them.

The robot is the consistent visual companion.

The world changes around it.

The interface stays minimal.

The engineering remains real.

The result should feel personal, technically impressive, cinematic, and unmistakably mine.

---

# 38. Source-of-Truth Rules for Implementation

When making design or implementation decisions, preserve these priorities:

1. **Story over template**
2. **Robot as the visual guide**
3. **Cream-white + power-blue robot in a warm, stylized natural world**
4. **Cinematic, stylized 3D built from simple shapes**
5. **Software + AI + robotics as interconnected disciplines**
6. **Non-linear / spatial storytelling rather than room-only structure**
7. **Real project content remains easy to access**
8. **Minimal UI**
9. **Performance matters**
10. **Accessibility matters**
11. **Animations should feel physical and intentional**
12. **Do not copy WALL-E, TVA, Apple, Caravan SandWitch, or any other reference literally**
13. **The final identity must be original**
14. **Do not invent biographical facts or project details**
15. **When information is missing, keep the structure flexible rather than fabricating content**

---

# 39. One-Sentence Definition

**An interactive cinematic 3D portfolio where a small cream-and-blue explorer robot guides visitors through a sunlit, stylized world of my interconnected software engineering, AI engineering, and robotics work.**
