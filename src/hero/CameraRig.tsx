import { useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { pointer, useHero } from './store'
import { CAM_POS, FOCUS_LEFT, FOCUS_RIGHT, TAN_BOTTOM, TAN_HALF_W, TAN_TOP, setLensWindow } from './heroCam'

const REF_SPAN = TAN_TOP - TAN_BOTTOM
const REF_MID = (TAN_TOP + TAN_BOTTOM) / 2
const MAX_SPAN = REF_SPAN * 1.3 // tallest view; past it, tall screens narrow instead
const ZOOM = 0.03 // leans in this much as the pointer swings the camera, so the key art's edges never show
const PIVOT = 5 // the camera orbits a point this far ahead: the near ground barely slides

/**
 * The hero camera. At rest it is exactly the key art's camera (heroCam.ts). The pointer
 * moves it a little (with a damped spring, never a snap) and turns it a touch toward the
 * pointer; a slow drift keeps the frame alive when the pointer is still.
 *
 * Framing on any screen: the key art's width is kept. A wider screen crops sky and
 * foreground evenly; a taller one keeps the foreground's bottom edge and shows a little more
 * sky, then (phones) narrows around Alu and the gate. Also updates the smoothed pointer and
 * the point where it meets the ground, used by Alu and the grass.
 */
export default function CameraRig() {
  const { camera, size } = useThree()
  const reduced = useHero((s) => s.reducedMotion)
  const vel = useRef(new THREE.Vector3())
  const pos = useRef(CAM_POS.clone())
  const tmp = useMemo(
    () => ({
      target: new THREE.Vector3(),
      ray: new THREE.Raycaster(),
      plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), 0),
      hit: new THREE.Vector3(),
      ndc: new THREE.Vector2(),
    }),
    [],
  )

  useFrame((state, dt) => {
    dt = Math.min(dt, 0.05)
    const t = state.clock.elapsedTime
    const cam = camera as THREE.PerspectiveCamera

    // ---- lens window for this screen
    const aspect = size.width / Math.max(1, size.height)
    let halfW = TAN_HALF_W
    let halfV = halfW / aspect
    if (2 * halfV > MAX_SPAN) {
      halfV = MAX_SPAN / 2
      halfW = halfV * aspect
    }
    const span = 2 * halfV
    const bottom = span <= REF_SPAN ? REF_MID - halfV : TAN_BOTTOM // wide: crop evenly; tall: keep the ground
    // narrow screens centre between Alu and the gate, never past the key art's edges
    const cx = THREE.MathUtils.clamp((FOCUS_LEFT + FOCUS_RIGHT) / 2, -TAN_HALF_W + halfW, TAN_HALF_W - halfW)
    // ---- smoothed pointer
    const k = 1 - Math.exp(-5 * dt)
    pointer.sx += (pointer.x - pointer.sx) * k
    pointer.sy += (pointer.y - pointer.sy) * k
    pointer.idle += dt

    // at rest the frame is exactly the key art; it leans in a touch as the camera swings
    const z = 1 - (reduced ? 0 : ZOOM * Math.min(1, Math.hypot(pointer.sx, pointer.sy * 0.8)))
    const midV = bottom + halfV
    setLensWindow(cam, cx - halfW * z, cx + halfW * z, midV - halfV * z, midV + halfV * z)

    // ---- spring toward the parallax offset
    const amp = reduced ? 0 : 1
    const goalX = CAM_POS.x + pointer.sx * 0.16 * amp + Math.sin(t * 0.21) * 0.02 * amp
    const goalY = CAM_POS.y + pointer.sy * 0.06 * amp + Math.sin(t * 0.17 + 1) * 0.012 * amp
    const goalZ = CAM_POS.z - Math.abs(pointer.sx) * 0.05 * amp
    const stiffness = 18
    const damping = 2 * Math.sqrt(stiffness) * 1.05
    vel.current.x += ((goalX - pos.current.x) * stiffness - vel.current.x * damping) * dt
    vel.current.y += ((goalY - pos.current.y) * stiffness - vel.current.y * damping) * dt
    vel.current.z += ((goalZ - pos.current.z) * stiffness - vel.current.z * damping) * dt
    pos.current.addScaledVector(vel.current, dt)
    cam.position.copy(pos.current)

    // orbit the pivot: level at rest; the far world (padded backdrop) does the travelling
    tmp.target.set(CAM_POS.x, CAM_POS.y, CAM_POS.z - PIVOT)
    cam.lookAt(tmp.target)
    cam.updateMatrixWorld()

    // ---- where the pointer ray meets the ground (y = 0)
    tmp.ndc.set(pointer.x, pointer.y)
    tmp.ray.setFromCamera(tmp.ndc, cam)
    if (tmp.ray.ray.intersectPlane(tmp.plane, tmp.hit)) {
      pointer.gx = tmp.hit.x
      pointer.gz = tmp.hit.z
    }
  })
  return null
}
