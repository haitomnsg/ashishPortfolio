import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame, type ThreeEvent } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { bubbleAnchor, pointer, useHero } from './store'

const ALU_URL = '/models/alu.glb'
const D = THREE.MathUtils.degToRad

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
      if (m.name === 'Alu_Glow') {
        if (o.name === 'Mast_Beacon') {
          const b = m.clone()
          b.emissiveIntensity = 2.2
          o.material = b
        } else {
          m.emissiveIntensity = 2.6
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
    nextWave: 2.4,
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
    const targetYaw = THREE.MathUtils.lerp(0.35, -D(28) + px * 0.55 + s.glance, turnIn)
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
      s.waveUntil = t + 2.3
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
    const hot = s.hover ? 3.4 : 2.6
    glowMats.current.forEach((m) => (m.emissiveIntensity += (hot - m.emissiveIntensity) * k(6)))

    // ---- blink ---------------------------------------------------------------------------
    if (t > s.blinkAt) {
      s.blink = 1
      s.blinkAt = t + 2.5 + Math.random() * 4
    }
    if (s.blink > 0) {
      s.blink = Math.max(0, s.blink - dt * 9)
      const open = s.blink > 0.5 ? 1 - (1 - s.blink) * 2 : s.blink * 2
      const sy = Math.max(0.08, 1 - (1 - open))
      eyes.forEach((e) => e.scale.setY(sy))
      scans.forEach((e) => e.scale.setY(sy))
    } else {
      eyes.forEach((e) => e.scale.setY(1))
      scans.forEach((e) => e.scale.setY(1))
    }

    // ---- hop on click ------------------------------------------------------------------
    if (s.hopV !== 0 || s.hop > 0) {
      s.hopV -= 11 * dt
      s.hop = Math.max(0, s.hop + s.hopV * dt)
      if (s.hop === 0) s.hopV = 0
    }
    if (root.current) {
      root.current.position.y = 0.5 + s.hop
      const squash = s.hop > 0 ? 1 + s.hop * 0.15 : 1
      root.current.scale.set(1 / Math.sqrt(squash), squash, 1 / Math.sqrt(squash))
    }
    const crouch = Math.min(0.25, s.hop * 0.4)
    ;[legR, legL].forEach((leg) => leg[1] && (leg[1].rotation.x = crouch))

    // ---- speech bubble anchor: project the top of the head to screen space --------------
    if (bubbleAnchor.el && root.current) {
      anchor.set(0.1, 1.42, 0).applyMatrix4(root.current.matrixWorld).project(state.camera)
      const w = state.size.width
      const h = state.size.height
      bubbleAnchor.el.style.transform = `translate3d(${((anchor.x + 1) / 2) * w}px, ${((1 - anchor.y) / 2) * h}px, 0)`
    }
  })

  return (
    <group ref={root} position={[-1.5, 0.5, 0.35]} rotation={[0, D(28), 0]}>
      <primitive object={scene} onPointerOver={onOver} onPointerOut={onOut} onClick={onClick} />
    </group>
  )
}

useGLTF.preload(ALU_URL)
