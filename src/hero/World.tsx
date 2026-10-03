import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { injectSea, injectSway, makeSwayUniforms } from './shaders'
import { env, pointer } from './store'

const WORLD_URL = '/models/world/hero.glb'

/**
 * The prop kit from docs/world/hero.blend. Every node keeps its Blender name, so this
 * component swaps in web materials by name and animates the pieces that should move:
 * clouds drift, the sea shimmers, grass and pines sway (grass also bends away from the
 * cursor), and the gate's light breathes and brightens when the pointer comes near.
 */
export default function World() {
  const { scene } = useGLTF(WORLD_URL)
  const clouds = useRef<THREE.Object3D[]>([])
  const cloudBase = useRef<number[]>([])
  const lights = useRef<THREE.MeshBasicMaterial[]>([])

  const mats = useMemo(() => {
    const paint = new THREE.MeshStandardMaterial({
      vertexColors: true,
      flatShading: true,
      roughness: 0.92,
      metalness: 0,
    })
    const grass = paint.clone()
    grass.side = THREE.DoubleSide
    const grassU = makeSwayUniforms(0.42, 0.045, 0.5)
    injectSway(grass, grassU)
    const pine = paint.clone()
    const pineU = makeSwayUniforms(0, 0.06, 5.0)
    injectSway(pine, pineU)
    const cloud = new THREE.MeshStandardMaterial({
      vertexColors: true,
      flatShading: true,
      roughness: 1,
      metalness: 0,
      emissive: new THREE.Color('#f4f8ff'),
      emissiveIntensity: 0.34,
    })
    const sea = new THREE.MeshStandardMaterial({
      vertexColors: true,
      flatShading: true,
      roughness: 0.5,
      metalness: 0,
      emissive: new THREE.Color('#2fc9c2'),
      emissiveIntensity: 0.38,
    })
    const seaU = { uTime: { value: 0 } }
    injectSea(sea, seaU)
    const glass = new THREE.MeshPhysicalMaterial({
      color: new THREE.Color('#cfeeff'),
      roughness: 0.06,
      metalness: 0,
      transparent: true,
      opacity: 0.15,
      envMapIntensity: 0.9,
      clearcoat: 1,
      clearcoatRoughness: 0.05,
      side: THREE.DoubleSide,
      depthWrite: false,
    })
    const light = () =>
      new THREE.MeshBasicMaterial({
        color: new THREE.Color('#fff1c9'),
        transparent: true,
        opacity: 0.08,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        side: THREE.DoubleSide,
        fog: false,
      })
    return { paint, grass, grassU, pine, pineU, cloud, sea, seaU, glass, light }
  }, [])

  useEffect(() => {
    clouds.current = []
    cloudBase.current = []
    lights.current = []
    scene.traverse((o) => {
      if (!(o instanceof THREE.Mesh)) return
      const name = o.name
      const matName = (o.material as THREE.Material).name
      o.castShadow = false
      o.receiveShadow = true
      if (name.startsWith('Tuft_')) {
        o.material = mats.grass
        o.frustumCulled = false
        o.castShadow = false
      } else if (/^Pine_\w+$/.test(name) && !name.endsWith('_Trunk')) {
        o.material = mats.pine
        o.castShadow = true
      } else if (matName === 'Cloud') {
        o.material = mats.cloud
        o.receiveShadow = false
        clouds.current.push(o)
        cloudBase.current.push(o.position.x)
      } else if (name === 'Sea') {
        o.material = mats.sea
        o.receiveShadow = false
      } else if (name === 'Gate_Glass') {
        o.material = mats.glass
        o.renderOrder = 5
      } else if (name === 'Gate_LightShaft' || name === 'Gate_Haze') {
        const m = mats.light()
        o.material = m
        o.renderOrder = 4
        o.receiveShadow = false
        lights.current.push(m)
      } else {
        o.material = mats.paint
        o.castShadow = !['Ground', 'Plateau', 'Cliff', 'Headland'].includes(name) && !name.startsWith('Crane')
      }
    })
  }, [scene, mats])

  const tmp = useMemo(() => new THREE.Vector3(), [])
  const envSeen = useRef(-1)
  useFrame((state) => {
    const t = state.clock.elapsedTime
    if (envSeen.current !== env.version && env.map) {
      envSeen.current = env.version
      mats.glass.envMap = env.map
      mats.glass.needsUpdate = true
    }
    mats.grassU.uTime.value = t
    mats.pineU.uTime.value = t
    mats.seaU.uTime.value = t
    tmp.set(pointer.gx, 0, pointer.gz)
    mats.grassU.uCursor.value.copy(tmp)
    clouds.current.forEach((c, i) => {
      c.position.x = cloudBase.current[i] + Math.sin(t * 0.05 + i) * 6 + t * 0.12 * (i === 0 ? 1 : 0.6)
    })
    // the gate's light: slow breath plus a lift when the pointer is near the gate
    const near = 1 - THREE.MathUtils.smoothstep(Math.hypot(pointer.gx, pointer.gz - 0.5), 1.5, 6)
    const breath = 0.11 + Math.sin(t * 0.8) * 0.025
    lights.current.forEach((m, i) => {
      m.opacity = THREE.MathUtils.lerp(m.opacity, breath + near * (i === 0 ? 0.12 : 0.06), 0.06)
    })
  })

  return <primitive object={scene} />
}

useGLTF.preload(WORLD_URL)
