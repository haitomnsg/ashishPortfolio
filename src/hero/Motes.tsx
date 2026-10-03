import { useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useFrame } from '@react-three/fiber'

const COUNT = 30

/** Dust motes drifting in the gate's light shaft (the one light source that may have particles). */
export default function Motes() {
  const ref = useRef<THREE.Points>(null)
  const { geometry, seeds } = useMemo(() => {
    const pos = new Float32Array(COUNT * 3)
    const seeds = new Float32Array(COUNT * 4)
    for (let i = 0; i < COUNT; i++) {
      seeds[i * 4] = Math.random()
      seeds[i * 4 + 1] = Math.random()
      seeds[i * 4 + 2] = Math.random()
      seeds[i * 4 + 3] = 0.4 + Math.random() * 0.8
    }
    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.BufferAttribute(pos, 3))
    return { geometry, seeds }
  }, [])
  const material = useMemo(
    () =>
      new THREE.PointsMaterial({
        color: new THREE.Color('#fff3d0'),
        size: 0.022,
        transparent: true,
        opacity: 0.55,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        sizeAttenuation: true,
      }),
    [],
  )
  useFrame((state) => {
    const t = state.clock.elapsedTime
    const a = geometry.getAttribute('position') as THREE.BufferAttribute
    for (let i = 0; i < COUNT; i++) {
      const s0 = seeds[i * 4], s1 = seeds[i * 4 + 1], s2 = seeds[i * 4 + 2], sp = seeds[i * 4 + 3]
      // inside the light in front of the opening: x widens toward the visitor (+z),
      // y from the terrace to the top of the glass
      const life = (t * 0.05 * sp + s2) % 1
      const z = 0.08 + life * 1.9
      const halfW = 0.5 + z * 0.2
      const x = (s0 * 2 - 1) * halfW + Math.sin(t * 0.7 + s1 * 9) * 0.06
      const y = 0.24 + s1 * 2.3 + Math.sin(t * 0.5 + s0 * 7) * 0.08
      a.setXYZ(i, x, y, z)
    }
    a.needsUpdate = true
    if (ref.current) (ref.current.material as THREE.PointsMaterial).opacity = 0.24 + Math.sin(t * 0.8) * 0.08
  })
  return <points ref={ref} geometry={geometry} material={material} frustumCulled={false} />
}
