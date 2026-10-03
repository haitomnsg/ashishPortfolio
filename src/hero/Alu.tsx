import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame, type ThreeEvent } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { bubbleAnchor, pointer, useHero } from './store'

const ALU_URL = '/models/alu.glb'
const D = THREE.MathUtils.degToRad
/** Where the key art has him: on the terrace left of the gate (docs/world/hero_build.py ALU). */
const HOME = new THREE.Vector3(-0.915, 0.181, 0.726)
const HOME_YAW = D(20)
const SIZE = 1.07 // the painted Alu is a little bigger than the model

/**
 * Alu, driven procedurally on the rest-pose GLB (DESIGN section 6 rig contract).
 * Blender axes map to three.js as: Blender X -> X, Blender Y -> -Z, Blender Z -> Y, so a
 * Blender rotation about Z is a three rotation about Y, and about Y is a three rotation
 * about -Z. The robot faces +Z here; the visitor's camera is at +Z.
 *
 * Behaviours: breathing, head follows the pointer (body follows a beat later), idle
 * glances, blinks, a looping wave that also fires on hover, flag and antenna sway, a
 * pulsing beacon, and a small hop on click.
 */
export default function Alu() {
  const { scene } = useGLTF(ALU_URL)
  const root = useRef<THREE.Group>(null)
  const setAluHover = useHero((s) => s.setAluHover)
  const setBubble = useHero((s) => s.setBubble)
  const reduced = useHero((s) => s.reducedMotion)

  const rig = useMemo(() => {
    const get = (n: string) => scene.getObjectByName(n) ?? null
    // remember rest transforms once (the GLTF scene is cached across remounts)
    scene.traverse((o) => {
      if (/^Eye_/.test(o.name) && !o.userData.rest) o.userData.rest = { scale: o.scale.clone(), y: o.position.y }
    })
    return {
      body: get('body'),
      neck: get('neck'),
      head: get('head'),
      antenna: get('antenna'),
      flag: get('Flag'),
      beacon: get('Mast_Beacon') as THREE.Mesh | null,
      eyes: ['Eye_L', 'Eye_R'].map(get).filter(Boolean) as THREE.Object3D[],
      scans: [0, 1, 2].flatMap((i) => [get(`Eye_L_Scan_${i}`), get(`Eye_R_Scan_${i}`)]).filter(Boolean) as THREE.Object3D[],
      armR: [get('arm_R_1'), get('arm_R_2'), get('arm_R_3')],
      armL: [get('arm_L_1'), get('arm_L_2'), get('arm_L_3')],
      legR: [get('leg_R_1'), get('leg_R_2'), get('leg_R_3')],
      legL: [get('leg_L_1'), get('leg_L_2'), get('leg_L_3')],
    }
  }, [scene])

  // materials: shadows on, hotter emissives for the bloom pass, the beacon on its own
  const glowMats = useRef<THREE.MeshStandardMaterial[]>([])
  useEffect(() => {
    glowMats.current = []
    scene.traverse((o) => {
      if (!(o instanceof THREE.Mesh)) return
      o.castShadow = true
      o.receiveShadow = true
      const m = o.material as THREE.MeshStandardMaterial
      if (m.name === 'Alu_Paint') {
        m.flatShading = true
        m.needsUpdate = true
      }
      if (m.name === 'Alu_Screen') m.color.set('#232846') // the painted face reads navy, not black
      if (m.name === 'Alu_Glow') {
        if (o.name === 'Mast_Beacon') {
          const b = m.clone()
          b.emissiveIntensity = 2.2
          o.material = b
        } else {
          // cyan with a soft bloom, not white: the diffuse stays low so light cannot wash it out
          m.color.set('#5fc4e2')
          m.emissiveIntensity = 0.85
          m.toneMapped = false
          if (!glowMats.current.includes(m)) glowMats.current.push(m)
        }
      }
    })
  }, [scene])

  // animation state kept out of React
  const st = useRef({
    t0: -1,
    headYaw: 0.35,
    headPitch: 0,
    bodyYaw: 0,
    wave: 0, // 0..1 blend toward the raised arm
    waveUntil: 0,
    nextWave: 0.9, // he is mid-wave in the key art: start with one
    blinkAt: 2.6,
    blink: 0,
    hop: 0,
    hopV: 0,
    glance: 0,
    glanceT: 0,
    hover: false,
  })

  const anchor = useMemo(() => new THREE.Vector3(), [])

  const onOver = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation()
    document.body.style.cursor = 'pointer'
    st.current.hover = true
    st.current.waveUntil = Infinity
    setAluHover(true)
    setBubble(true)
  }
  const onOut = () => {
    document.body.style.cursor = ''
    st.current.hover = false
    st.current.waveUntil = 0
    setAluHover(false)
  }
  const onClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation()
    if (st.current.hop <= 0.001) st.current.hopV = 2.6
    setBubble(true)
  }

  useFrame((state, dt) => {
    const s = st.current
    const t = state.clock.elapsedTime
    if (s.t0 < 0) {
      s.t0 = t
      // the bubble opens about 1.2 s after the scene appears (DESIGN section 8)
      window.setTimeout(() => setBubble(true), 1200)
    }
    const age = t - s.t0
    dt = Math.min(dt, 0.05)
    const k = (rate: number) => 1 - Math.exp(-rate * dt)
    const { body, neck, head, antenna, flag, beacon, eyes, scans, armR, armL, legR, legL } = rig

    // ---- head follows the pointer; body follows a beat later --------------------------
    const turnIn = THREE.MathUtils.smoothstep(age, 0.6, 1.5) // turns to the visitor at ~0.6 s
    const idle = pointer.idle
    if (idle > 4 && t > s.glanceT) {
      s.glance = (Math.random() - 0.5) * 0.8
      s.glanceT = t + 2.5 + Math.random() * 3
    }
    if (idle < 4) s.glance = 0
    const px = reduced ? 0 : pointer.sx
    const py = reduced ? 0 : pointer.sy
    // the head faces the visitor, turned a little toward the gate as painted
    const targetYaw = THREE.MathUtils.lerp(0.35, -D(8) + px * 0.55 + s.glance, turnIn)
    const targetPitch = THREE.MathUtils.lerp(0.05, -py * 0.28 + 0.04, turnIn)
    s.headYaw += (targetYaw - s.headYaw) * k(7)
    s.headPitch += (targetPitch - s.headPitch) * k(7)
    s.bodyYaw += (s.headYaw * 0.22 - s.bodyYaw) * k(2.6)
    if (head) {
      head.rotation.set(s.headPitch, s.headYaw, Math.sin(t * 0.9) * 0.012)
    }
    if (neck) neck.rotation.y = s.bodyYaw * 0.5
    if (body) {
      body.rotation.y = s.bodyYaw
      const breath = reduced ? 0 : 1 + Math.sin(t * 1.6) * 0.012
      body.scale.set(1, breath, 1)
    }

    // ---- wave: loops every few seconds, held while hovered -----------------------------
    if (!reduced && t > s.nextWave && s.waveUntil < t) {
      s.waveUntil = t + (s.nextWave < 1 ? 3.4 : 2.3)
      s.nextWave = t + 7 + Math.random() * 4
    }
    const waving = t < s.waveUntil
    s.wave += ((waving ? 1 : 0) - s.wave) * k(waving ? 9 : 4)
    const w = s.wave
    const osc = Math.sin(t * (s.hover ? 11 : 8.5)) * w
    if (armR[0]) armR[0].rotation.set(THREE.MathUtils.lerp(0.05, -D(25), w), 0, THREE.MathUtils.lerp(-0.08, -D(100), w))
    if (armR[1]) armR[1].rotation.set(0, 0, THREE.MathUtils.lerp(-0.1, -D(48), w) + osc * 0.32)
    if (armR[2]) armR[2].rotation.set(0, THREE.MathUtils.lerp(0, -D(30), w), THREE.MathUtils.lerp(0, -D(10), w) + osc * 0.18)
    if (armL[0]) armL[0].rotation.set(0.12 + Math.sin(t * 1.6) * 0.02, 0, 0.1)
    if (armL[1]) armL[1].rotation.set(0, 0, 0.18)
    if (armL[2]) armL[2].rotation.set(0, D(20), 0)

    // ---- flag, antenna, beacon ---------------------------------------------------------
    if (flag) flag.rotation.y = Math.sin(t * 2.4) * 0.14 + Math.sin(t * 5.1) * 0.05 + s.headYaw * 0.25
    if (antenna) antenna.rotation.x = Math.sin(t * 3.1) * 0.03 + s.headPitch * 0.3
    if (beacon) {
      const m = beacon.material as THREE.MeshStandardMaterial
      m.emissiveIntensity = 1.4 + (Math.sin(t * 2.2) * 0.5 + 0.5) * 1.6
    }
    const hot = s.hover ? 1.15 : 0.85
    glowMats.current.forEach((m) => (m.emissiveIntensity += (hot - m.emissiveIntensity) * k(6)))

    // ---- blink ---------------------------------------------------------------------------
    if (t > s.blinkAt) {
      s.blink = 1
      s.blinkAt = t + 2.5 + Math.random() * 4
    }
    if (s.blink > 0) {
      s.blink = Math.max(0, s.blink - dt * 9)
      const open = s.blink > 0.5 ? 1 - (1 - s.blink) * 2 : s.blink * 2
      lid(eyes, scans, Math.max(0.08, open))
    } else {
      lid(eyes, scans, 1)
    }

    // ---- hop on click ------------------------------------------------------------------
    if (s.hopV !== 0 || s.hop > 0) {
      s.hopV -= 11 * dt
      s.hop = Math.max(0, s.hop + s.hopV * dt)
      if (s.hop === 0) s.hopV = 0
    }
    if (root.current) {
      root.current.position.y = HOME.y + s.hop
      const squash = s.hop > 0 ? 1 + s.hop * 0.15 : 1
      root.current.scale.set(SIZE / Math.sqrt(squash), SIZE * squash, SIZE / Math.sqrt(squash))
    }
    const crouch = Math.min(0.25, s.hop * 0.4)
    ;[legR, legL].forEach((leg) => leg[1] && (leg[1].rotation.x = crouch))

    // ---- speech bubble anchor: project the top of the head to screen space --------------
    if (bubbleAnchor.el && root.current) {
      // just left of the mast top, where the key art's bubble tail points
      anchor.set(-0.28, 1.22, -0.1).applyMatrix4(root.current.matrixWorld).project(state.camera)
      const w = state.size.width
      const h = state.size.height
      const x = ((anchor.x + 1) / 2) * w
      bubbleAnchor.el.style.transform = `translate3d(${x}px, ${((1 - anchor.y) / 2) * h}px, 0)`
      // the card sits up and to the left of the tail; on narrow screens slide it back on
      // screen and move the tail the other way so it still points at Alu
      const shift = Math.max(0, 12 - (x - (bubbleAnchor.width - 64)))
      bubbleAnchor.el.style.setProperty('--shift', `${shift.toFixed(1)}px`)
    }
  })

  return (
    <group ref={root} position={HOME} rotation={[0, HOME_YAW, 0]} scale={SIZE}>
      <primitive object={scene} onPointerOver={onOver} onPointerOut={onOut} onClick={onClick} />
    </group>
  )
}

/**
 * Opens the eyes to `k` (1 = open). Each eye is a flat disc turned to face forward, so its
 * height is its local Z; the scanlines close in toward the eye's centre.
 */
function lid(eyes: THREE.Object3D[], scans: THREE.Object3D[], k: number) {
  eyes.forEach((e) => {
    const r = e.userData.rest
    if (r) e.scale.set(r.scale.x, r.scale.y, r.scale.z * k)
  })
  scans.forEach((sc) => {
    const r = sc.userData.rest
    const eye = sc.name.startsWith('Eye_L') ? eyes[0] : eyes[1]
    const cy = eye?.userData.rest?.y ?? r?.y ?? 0
    if (r) {
      sc.scale.y = r.scale.y * k
      sc.position.y = cy + (r.y - cy) * k
    }
  })
}

useGLTF.preload(ALU_URL)
