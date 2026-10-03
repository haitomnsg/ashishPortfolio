# Ashish Gupta — Profile Research (source of facts for the portfolio)

> Compiled 2026-09-30 from: `README.md` (vision), haitomns.dev (all pages), github.com/haitomnsg
> (profile README + 104 repos), the LaTeX CV at `haitomnsg/ashishGuptaCV`, and the public parts of
> Instagram/Facebook. LinkedIn is behind an auth wall; the CV was used for career facts instead.
> **Rule from the vision doc:** never invent biographical facts. Everything below is sourced.

## 1. Identity

| Field | Value | Source |
|---|---|---|
| Name | Ashish Gupta | site, GitHub, CV |
| Handle | `haitomnsg` everywhere (GitHub, IG, FB, LinkedIn) | site footer |
| Location | Birgunj, Parsa, Nepal (studies in Dhulikhel, Kavre) | GitHub, CV |
| Self-description (current) | "AI & Robotics Engineer" / "Programmer interested in AI, ML and Robotics" | site, GitHub bio |
| Target self-description (vision) | Robotics Engineer · Software Engineer · AI Engineer, as one converged identity | README §1, §7 |
| Email | haitomns@gmail.com | site contact, CV |
| Phone | +977 980 920 4764 | site contact |
| Domain | haitomns.dev (GitHub Pages, SPA, deep links currently 404) | observed |
| Personal touch | Instagram bio: "Kinda like Alu 🥔" (alu = potato). Candidate robot name. | Instagram |
| Languages | English (professional), Nepali (native), Hindi (working) | CV |
| Pronouns | he/his | Instagram |
| LinkedIn headline | "BTech AI Student @ Kathmandu University · Robotics & Full-Stack Engineer · Published Researcher · EncodeX Intern" (855 followers, 500+ connections) | LinkedIn (via Chrome) |
| Frequent collaborator | Rubina Dangol Maharjan (TomatoBot, JeevI, Phulbari, DocLipi, Recyclo, Jiffy, DizzyBits) | LinkedIn |
| Supervisors / mentors | Sandesh Thakuri, Yagya Raj Pandeya PhD, Manoj Shakya PhD (KU Dept. of AI) | LinkedIn |
| Personal photography | Outdoor Nepal: lakes, terraced hills, Himalayan skylines, pine forests, prayer flags, one 3D-printer shot. Natural light, calm, cool blues and greens. No neon anywhere. | Instagram grid |
| Facebook | Profile exists, no public posts | Facebook |
| Existing mark | Black circle monogram, geometric single-stroke line construction | site logo |
| Photo | Black-and-white portrait, hoodie, glasses | site home |

## 2. Timeline (facts only — present as converging paths, not a ladder)

| When | What | Domain(s) |
|---|---|---|
| ~Class 9 | Started programming **and** robotics at the same time | SW + Robotics (README §7–8) |
| 2019 – 2023 | Diploma in Computer Engineering, Shree Nrisingh Madhyamik Vidyalaya, Birgunj (GPA 3.60; TSEE 2021 GPA 4.0) | SW |
| 2021-06 | Earliest public repos: C school-management systems, Python/Dart/Java practice | SW |
| 2021-03 → 2023-01 | Blogger at High Approach | — |
| 2022-08 | tournamenthub, captiveRestro, pharmear (first shipped products) | SW |
| 2022-09 → present | **Head of Development, Haitomns Groups Pvt. Ltd.** — 10+ clients; RedSoil, RestHat, WadaConnect | SW |
| 2022-10 | RedSoil (blood bank desktop app, JavaFX) in real use at a local blood bank | SW |
| 2023 | AAVISHKAR (KU Robotics Club) 1st runner-up — vacuum-cleaner robot in 24 h | Robotics |
| 2023-06 | OnBoard PCB (home-automation board) | Hardware |
| 2023-11 → 2027-11 (expected) | **B.Tech in Artificial Intelligence, Kathmandu University** | AI |
| 2024-05 | Phulbari (CNN flower classifier + ESP32 irrigation) | AI + IoT |
| 2024 | CodeFest 2024 (Code for Change) 2nd place; JIFFY Hackathon 2024 2nd place → Jiffy app | SW + AI |
| 2024-12 | TomatoBot v2 (YOLOv11, 88% real-world accuracy, Android control app) | Robotics + AI + SW |
| 2025 | JeevI — 12-DOF quadruped, PPO in NVIDIA Isaac Lab; hardware with KU Robotics Club | Robotics + AI |
| 2025-05 | DocLipi (DenseNet121 + Gemma 3 Vision, JavaFX + FastAPI) | AI + SW |
| 2025 | Global IME AI/ML Hackathon — Best Presentation; Mentor certification, KU Robotics Club | — |
| 2025-12 | ICT Award 2025 Rising Star Innovation — semi-finalist (Phulbari, top 13) | — |
| 2026-01 | **Published**: "TomatoBot: Edge-Optimized Autonomous Tomato Harvesting Robot", IJICTDC (ISSN 2466-0094 / 2508-2620), co-author Rubina Dangol Maharjan, supervised by Sandesh Thakuri & Yagya Raj Pandeya PhD | Robotics + AI |
| 2026-03 → present | **Full Stack Engineer Intern, EncodeX** (remote) — AI automation, Flutter, Django; hired off an international hackathon | SW + AI |
| 2026-04 | Harvard Health Hackathon — Top 20 (team DizzyBits, "DementiaBot"), 2nd in regional round | AI + SW |
| 2025-06 | Recyclo (Next.js + Gemini) built in June 2025; ArthaVidhi 2025–26 | SW + AI |
| 2026-07 (approx.) | AI/ML Intelligence Hackathon 2026 (Guru Technology) — **2nd place**, team DizzyBits: explainable account-risk scoring on transaction data (XGBoost, ranked review queue). Repo `riskScoring`. | AI |
| 2026-09-30 | `ashishPortfolio` repo created — "My Personal 3D Portfolio Website" | this project |

GitHub activity: 2,516 contributions in the last year, 367 followers, 62 repos contributed to.

## 3. Projects — canonical list for the site

Grouped by *primary* environment, but each spans several domains (README §11). Tags = which
paths intersect. ★ = worth a full "scene"; the rest are path-side artifacts.

### Robotics (physical machines)
- ★ **TomatoBot / TomatoBot v2** — autonomous harvesting robot. YOLO (v8→v11) ripeness detection (6 classes, 88%), U-Net path segmentation, Deep Hough Transform line estimation, 6-DOF arm with inverse kinematics, Raspberry Pi, Java Android app (manual + autonomous). *Published paper.* Photo exists on current site. Tags: Robotics · AI · SW.
- ★ **JeevI / JeevI-II ("SPDR Bot")** — 3D-printable 12-DOF quadruped, PPO locomotion policy trained in NVIDIA Isaac Lab; converged on flat (+256.27), rough (+191.83) and obstacle (+184.05) terrain. URDF/USD/STL assets exist in repo `jeevi-ii` → a real robot mesh we can show in-browser. Tags: Robotics · AI.
- **Face & Human Tracking Robot** — Arduino + MU vision sensor; dual mode (person following / traffic-sign following). Tags: Robotics · AI.
- **Multi-Utility Disaster Rescue Vehicle** — Arduino, robotic arm, drone, fire suppression, camera. Tags: Robotics.
- **Arduino Obstacle-Avoiding Car** — ultrasonic scan-and-choose navigation (early work). Tags: Robotics.
- **Vacuum-cleaner robot** (AAVISHKAR 2023, 24 h build). Tags: Robotics.
- Also on GitHub, sparse detail: `CampusRobot`, `bionicHand`, `OnBoardPCB` (home-automation PCB).

### AI / ML (intelligence)
- ★ **DocLipi** — bank document classifier + Nepali/English OCR + person-wise grouping + natural-language SQL querying. DenseNet121, Gemma 3 Vision, JavaFX desktop + FastAPI. Screenshots exist. Tags: AI · SW.
- ★ **Phulbari** — 100-species flower CNN (ResNet-50 / VGG-16), care tips, disease detection, ESP32 soil-moisture irrigation synced to Firebase. ICT Award semi-finalist. Tags: AI · IoT/Robotics · SW.
- **Recyclo** — AI waste classification, reuse ideas, thrift exchange, cleanup events, leaderboard. Next.js + Gemini. Tags: AI · SW.
- **DementiaBot** (Harvard Health Hackathon, Top 20). Tags: AI · SW. *(Limited detail — do not embellish.)*
- Coursework/experiments (a "lab bench" wall, not individual scenes): brain-tumor area estimation, fire/smoke detection network, anomaly detection autoencoders, DQN, LSTM/GRU/seq2seq, Nepali NLP, Nepali fake news, Nepali song classification, audio classification, optical flow, panoptic segmentation, heritage classification, risk scoring, Bitcoin time series, morphological image processing.

### Software (systems in production)
- ★ **ArthaVidhi** — SME billing & business management: VAT-compliant invoicing, inventory, expenses, quotations, attendance, PDF reports. Next.js App Router, TypeScript, ShadCN, MySQL. Screenshots exist. Tags: SW.
- **RestHat** — restaurant management: live orders dashboard, menu, waiter module, kitchen, IRD-certified billing (Nepal tax authority), dual-printer receipts; deployed to multiple clients. PHP/MySQL. Screenshots exist. Tags: SW.
- **RedSoil** — blood-bank inventory desktop app, in real use, 30% wastage reduction via expiry alerts. JavaFX/MySQL. Screenshots exist. Tags: SW.
- **WadaConnect** — digital governance platform for ward offices (citizen registration, document requests, tracking). Tags: SW. *(CV only; no visuals yet.)*
- **Jiffy (jiffify)** — redesigned food-delivery Android app: Gemini recommendations, ARCore menu viewing, games, shorts. Hackathon 2nd place. Tags: SW · AI.
- **irdBillSync** — PHP integration for Nepal's IRD Central Billing system (open-source utility). Tags: SW.
- Others: pharmear, tournamenthub, crm, mstView, healthGurdian, kurcInventory.

## 4. Skills (only what is evidenced by repos/CV)

- **Languages:** Python, Java, TypeScript/JavaScript, C, C++, C#, PHP, SQL, Dart, LaTeX
- **Web/Full-stack:** React, Next.js, Node/Express, Django, FastAPI, Flask, Vite, Tailwind, ShadCN
- **Mobile:** Android (Java), Flutter, ARCore/Sceneform
- **Desktop:** JavaFX, Qt, .NET/Blazor, C# WinForms
- **AI/ML:** TensorFlow, Keras, PyTorch, YOLO v8/v11, U-Net, DenseNet/ResNet/VGG, OpenCV, scikit-learn, PPO (rsl_rl / skrl), Gemini & Gemma APIs
- **Robotics/Hardware:** Raspberry Pi, Arduino, ESP32, ROS/URDF, NVIDIA Isaac Lab / Isaac Sim, inverse kinematics, servo/motor drivers, ultrasonic & vision sensors, 3D printing (Fusion 360 meshes)
- **Data/Cloud:** MySQL, MongoDB, Firebase, Supabase, Docker, GitHub Actions, Jenkins, AWS/GCP/Azure (badges only — verify before featuring)
- **Design:** Figma, Canva, Lightroom

## 5. Voice & personality cues

- Writes plainly, first person, names products with Nepali words (ArthaVidhi, Phulbari, DocLipi — *lipi* = script, JeevI — *jeev* = life). Keep the Nepali naming; it is distinctive.
- Solves *local, real* problems: blood banks, restaurants, ward offices, tomato farms, Nepali OCR. This is the through-line: "machines and software for problems I can see from where I stand."
- Self-deprecating humour ("Kinda like Alu 🥔"). The robot can carry that warmth.
- Ships to real users (RedSoil, RestHat clients), competes (7 placements), publishes (1 paper). Confident, not corporate.

## 6. Current site — keep vs. drop

Keep: the six project write-ups and screenshots, the robotics descriptions, contact details, the
monogram, the black-and-white portrait, the plain first-person voice.

Drop: sidebar-dashboard layout, pastel tri-colour skill cards, tag-pill overload, "Programmed with ❤️"
footer, the split between Projects and Robotics pages (it separates what the vision wants merged),
broken deep links on GitHub Pages.

## 7. Open gaps (ask Ashish; do not fabricate)

1. Robot name: **Alu** is the working name on the model, renders and hero mockups; a final yes is still open.
2. Preferred identity order: "Robotics · Software · AI" vs "Software · AI · Robotics".
3. Photos/videos: `public/images/` now holds files named for TomatoBot (`tomato-bot.jpg`,
   `tomato-bot-v2.jpg`, `tomato-bot-robot.jpg`), the face-tracking robot, the rescue vehicle and the
   obstacle-avoiding car, plus app screenshots for ArthaVidhi, DocLipi, Jiffy, Phulbari, RedSoil and
   RestHat. Still missing: JeevI hardware, the OnBoard PCB, any video.
4. WadaConnect and DementiaBot: any screenshots or public links?
5. Which projects may show client names (RedSoil blood bank, RestHat restaurants)?
6. Keep GitHub Pages hosting (needs a SPA 404 fallback) or move to Vercel/Cloudflare Pages?

## 8. Engineering evidence available (Ashish, 2026-10-03)

For callouts and redrawn charts (DESIGN §11):
- **CAD / 3D:** Fusion 360 files; Blender meshes; Isaac Lab / URDF robot descriptions (e.g. JeevI in
  `jeevi-ii`).
- **Graphs & logs:** training curves, reward plots, detection results, terminal output. Charts are
  redrawn in site style from the raw numbers (TensorBoard/CSV exports).
