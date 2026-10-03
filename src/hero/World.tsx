import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useTexture } from '@react-three/drei'
import { glassMaterial, injectProjection, injectSway, makeSwayUniforms } from './shaders'
import { PLATE_URL, restViewProjection } from './heroCam'
import { pointer } from './store'

const WORLD_URL = '/models/world/hero.glb'

/**
 * The near world from docs/world/hero.blend. Materials are swapped by name:
 * - "Proj": proxy meshes painted by projecting the key-art plate from the rest camera
 *   (terrace, ground, step, rocks, pines, the gate frame). Pines also sway in the wind.
 * - "World_Paint": the grass tufts (painted in Blender), swaying and bending from the cursor.
 * - "Gate_Glass" / "Gate_Light": the glass and the light it spills, which breathe and
 *   brighten when the pointer comes near the gate.
 */
export default function World() {
  const { scene } = useGLTF(WORLD_URL)
  const plate = useTexture(PLATE_URL)
  const gl = useThree((s) => s.gl)
  const lights = useRef<THREE.MeshBasicMaterial[]>([])

  useEffect(() => {
    plate.colorSpace = THREE.SRGBColorSpace
    plate.anisotropy = Math.min(8, gl.capabilities.getMaxAnisotropy())
    plate.needsUpdate = true
  }, [plate, gl])

  const mats = useMemo(() => {
    const proj = { uPlate: { value: plate as THREE.Texture }, uProjVP: { value: restViewProjection() } }
    const painted = new THREE.MeshBasicMaterial({ vertexColors: true })
    injectProjection(painted, proj)
    const pineU = makeSwayUniforms(0, 0.035, 3.0)
    const pine = new THREE.MeshBasicMaterial({ vertexColors: true })
    injectProjection(pine, proj, pineU)

    // tufts carry their paint (sunlit side, shade, darker base) in vertex colours
    const grass = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide })
    const grassU = makeSwayUniforms(0.12, 0.012, 0.18)
    injectSway(grass, grassU)

    const glass = glassMaterial()
    const light = () =>
      new THREE.MeshBasicMaterial({
        color: new THREE.Color('#fff1c9'),
        transparent: true,
        opacity: 0.05,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        side: THREE.DoubleSide,
        fog: false,
      })
    return { painted, pine, pineU, grass, grassU, glass, light }
  }, [plate])

  useEffect(() => {
    lights.current = []
    scene.traverse((o) => {
      if (!(o instanceof THREE.Mesh)) return
      const name = o.name
      const matName = (o.material as THREE.Material).name
      o.castShadow = false
      o.receiveShadow = false
      if (matName === 'Proj') {
        o.material = /^Pine_[LR]$/.test(name) ? mats.pine : mats.painted
      } else if (name.startsWith('Tuft_')) {
        o.material = mats.grass
        o.frustumCulled = false
      } else if (name === 'Gate_Glass') {
        o.material = mats.glass
        o.renderOrder = 5
      } else if (name === 'Gate_LightShaft') {
        const m = mats.light()
        o.material = m
        o.renderOrder = 4
        lights.current.push(m)
      } else if (name === 'Gate_Haze') {
        o.visible = false // the glass shader carries the glow now
      }
    })
  }, [scene, mats])

  const tmp = useMemo(() => new THREE.Vector3(), [])
  useFrame((state) => {
    const t = state.clock.elapsedTime
    mats.grassU.uTime.value = t
    mats.pineU.uTime.value = t
    tmp.set(pointer.gx, 0, pointer.gz)
    mats.grassU.uCursor.value.copy(tmp)
    // the gate's light: slow breath plus a lift when the pointer is near the gate
    const near = 1 - THREE.MathUtils.smoothstep(Math.hypot(pointer.gx, pointer.gz - 0.5), 0.8, 3.5)
    const glass = mats.glass.uniforms
    glass.uTime.value = t
    glass.uGlow.value += (near - glass.uGlow.value) * 0.06
    const breath = 0.05 + Math.sin(t * 0.8) * 0.015
    lights.current.forEach((m) => {
      m.opacity = THREE.MathUtils.lerp(m.opacity, breath + near * 0.06, 0.06)
    })
  })

  return <primitive object={scene} />
}

useGLTF.preload(WORLD_URL)
useTexture.preload(PLATE_URL)
