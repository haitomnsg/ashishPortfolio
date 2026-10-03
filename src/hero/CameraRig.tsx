import { useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { pointer, useHero } from './store'

const BASE = new THREE.Vector3(0.3, 2.0, 12.2) // matches Hero_Cam in docs/world/hero.blend
const TARGET = new THREE.Vector3(0.1, 2.05, 0)
const HFOV = 2 * Math.atan(18 / 34) // 34 mm lens on a 36 mm sensor

/**
 * Camera parallax: the pointer moves the camera a little (and the look target less), with
 * a damped spring so it never snaps. A slow drift keeps the frame alive with no pointer.
 * Also updates the smoothed pointer and the ground hit used by Alu and the grass.
 */
export default function CameraRig() {
  const { camera, size } = useThree()
  const reduced = useHero((s) => s.reducedMotion)
  const vel = useRef(new THREE.Vector3())
  const pos = useRef(BASE.clone())
  const tmp = useMemo(
    () => ({ target: new THREE.Vector3(), ray: new THREE.Raycaster(), plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit: new THREE.Vector3(), ndc: new THREE.Vector2() }),
    [],
  )

  useFrame((state, dt) => {
    dt = Math.min(dt, 0.05)
    const t = state.clock.elapsedTime
    const cam = camera as THREE.PerspectiveCamera

    // keep the gate framed on any aspect: constant horizontal FOV, clamped vertically
    const aspect = size.width / Math.max(1, size.height)
    const vfov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(HFOV / 2) / aspect))
    const want = THREE.MathUtils.clamp(vfov, 38.9, 70)
    if (Math.abs(cam.fov - want) > 0.01) {
      cam.fov = want
      cam.updateProjectionMatrix()
    }

    // smoothed pointer
    const k = 1 - Math.exp(-5 * dt)
    pointer.sx += (pointer.x - pointer.sx) * k
    pointer.sy += (pointer.y - pointer.sy) * k
    pointer.idle += dt

    // where the pointer ray meets the ground (y = 0)
    tmp.ndc.set(pointer.x, pointer.y)
    tmp.ray.setFromCamera(tmp.ndc, cam)
    if (tmp.ray.ray.intersectPlane(tmp.plane, tmp.hit)) {
      pointer.gx = tmp.hit.x
      pointer.gz = tmp.hit.z
    }

    // spring toward the parallax offset
    const amp = reduced ? 0 : 1
    const drift = reduced ? 0 : 1
    const goalX = BASE.x + pointer.sx * 0.55 * amp + Math.sin(t * 0.21) * 0.08 * drift
    const goalY = BASE.y + pointer.sy * 0.28 * amp + Math.sin(t * 0.17 + 1) * 0.05 * drift
    const goalZ = BASE.z - Math.abs(pointer.sx) * 0.2 * amp
    const stiffness = 18
    const damping = 2 * Math.sqrt(stiffness) * 1.05
    const ax = (goalX - pos.current.x) * stiffness - vel.current.x * damping
    const ay = (goalY - pos.current.y) * stiffness - vel.current.y * damping
    const az = (goalZ - pos.current.z) * stiffness - vel.current.z * damping
    vel.current.x += ax * dt
    vel.current.y += ay * dt
    vel.current.z += az * dt
    pos.current.x += vel.current.x * dt
    pos.current.y += vel.current.y * dt
    pos.current.z += vel.current.z * dt
    cam.position.copy(pos.current)

    tmp.target.set(TARGET.x + pointer.sx * 0.25 * amp, TARGET.y + pointer.sy * 0.12 * amp, TARGET.z)
    cam.lookAt(tmp.target)
  })
  return null
}
