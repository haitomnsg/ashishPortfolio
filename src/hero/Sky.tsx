import { useEffect, useMemo } from 'react'
import * as THREE from 'three'
import { useThree } from '@react-three/fiber'
import { skyMaterial } from './shaders'
import { env } from './store'

/**
 * The gradient dome the camera sees. The same gradient is rendered once into a small
 * cube map that only the gate's glass reflects (never a scene-wide environment light,
 * which would wash out the flat colours and fill the shadows).
 */
export default function Sky() {
  const gl = useThree((s) => s.gl)
  const mat = useMemo(() => skyMaterial(), [])

  useEffect(() => {
    const scene = new THREE.Scene()
    const dome = new THREE.Mesh(new THREE.SphereGeometry(50, 24, 12), skyMaterial())
    scene.add(dome)
    const rt = new THREE.WebGLCubeRenderTarget(128, { type: THREE.HalfFloatType })
    const cam = new THREE.CubeCamera(0.1, 100, rt)
    cam.update(gl, scene)
    env.map = rt.texture
    env.version++
    return () => {
      rt.dispose()
      dome.geometry.dispose()
      ;(dome.material as THREE.Material).dispose()
      env.map = null
    }
  }, [gl])

  return (
    <mesh material={mat} renderOrder={-10} frustumCulled={false}>
      <sphereGeometry args={[800, 32, 16]} />
    </mesh>
  )
}
