import { useEffect, useMemo } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import { backdropMaterial } from './shaders'
import { BACKDROP } from './heroCam'

/**
 * The far world: the matte painting made from the key art by docs/world/backdrop_build.py
 * (sky, the big cloud, the headland and its crane, the sea), on a dome at infinity. It is
 * mapped by view direction exactly as the rest camera saw it, so when the camera moves
 * it behaves like a distant view and the near world slides across it.
 */
export default function Sky() {
  const map = useTexture(BACKDROP.url)
  const gl = useThree((s) => s.gl)
  const mat = useMemo(() => backdropMaterial(map), [map])

  useEffect(() => {
    map.colorSpace = THREE.SRGBColorSpace
    map.anisotropy = Math.min(8, gl.capabilities.getMaxAnisotropy())
    map.needsUpdate = true
  }, [map, gl])

  useFrame((state) => {
    mat.uniforms.uTime.value = state.clock.elapsedTime
  })

  return (
    <mesh material={mat} renderOrder={-10} frustumCulled={false}>
      <sphereGeometry args={[800, 48, 24]} />
    </mesh>
  )
}

useTexture.preload(BACKDROP.url)
