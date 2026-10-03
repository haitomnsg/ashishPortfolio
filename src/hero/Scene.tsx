import { Suspense, useEffect, useMemo } from 'react'
import * as THREE from 'three'
import { Canvas, useThree } from '@react-three/fiber'
import { useProgress } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import Sky from './Sky'
import World from './World'
import Alu from './Alu'
import CameraRig from './CameraRig'
import Motes from './Motes'
import { useHero } from './store'

function Ready() {
  const { active, progress } = useProgress()
  const setReady = useHero((s) => s.setReady)
  useEffect(() => {
    if (!active && progress >= 100) {
      const id = window.setTimeout(() => setReady(true), 120)
      return () => window.clearTimeout(id)
    }
  }, [active, progress, setReady])
  return null
}

function Atmosphere() {
  const scene = useThree((s) => s.scene)
  const fog = useMemo(() => new THREE.Fog('#cfeaf7', 110, 560), [])
  useEffect(() => {
    scene.fog = fog
    return () => {
      scene.fog = null
    }
  }, [scene, fog])
  return null
}

/**
 * Reference lighting from DESIGN section 3: warm sun from the upper left and front, a
 * blue-violet sky fill so shadows never go black. No tone mapping: colours stay flat and
 * saturated like the Blender "Standard" renders.
 */
export default function Scene() {
  return (
    <Canvas
      shadows
      dpr={[1, 1.5]}
      camera={{ fov: 38.9, near: 0.1, far: 1500, position: [0.3, 2.0, 12.2] }}
      gl={{
        antialias: true,
        toneMapping: THREE.NoToneMapping,
        outputColorSpace: THREE.SRGBColorSpace,
        powerPreference: 'high-performance',
      }}
      onCreated={(state) => {
        state.gl.shadowMap.type = THREE.PCFSoftShadowMap
        if (import.meta.env.DEV) (window as unknown as { __r3f: unknown }).__r3f = state
      }}
    >
      <Atmosphere />
      <directionalLight
        color="#ffe3bc"
        intensity={2.8}
        position={[-5, 6.2, 3.2]}
        castShadow
        shadow-mapSize={[1536, 1536]}
        shadow-bias={-0.0004}
        shadow-normalBias={0.02}
        shadow-camera-near={1}
        shadow-camera-far={40}
        shadow-camera-left={-11}
        shadow-camera-right={11}
        shadow-camera-top={9}
        shadow-camera-bottom={-9}
      />
      <hemisphereLight color="#9db4ea" groundColor="#dcc8a6" intensity={0.75} />
      <Suspense fallback={null}>
        <Sky />
        <World />
        <Alu />
        <Motes />
        <Ready />
      </Suspense>
      <CameraRig />
      <EffectComposer multisampling={2}>
        <Bloom luminanceThreshold={1.15} mipmapBlur intensity={0.5} radius={0.5} />
      </EffectComposer>
    </Canvas>
  )
}
