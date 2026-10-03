import { Suspense, useEffect } from 'react'
import * as THREE from 'three'
import { Canvas } from '@react-three/fiber'
import { useProgress } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import Sky from './Sky'
import World from './World'
import Alu from './Alu'
import CameraRig from './CameraRig'
import Motes from './Motes'
import { useHero } from './store'
import { CAM_POS } from './heroCam'

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

/**
 * The near and far world are painted (projected from the key art), so lights only touch
 * what is truly 3D: Alu and the grass tufts. They copy the key art's light on Alu: a warm
 * key from the upper left and front, a blue sky fill so shade never goes grey, and the
 * gate's warm glow on his right side. No tone mapping: colours stay as painted.
 */
export default function Scene() {
  return (
    <Canvas
      dpr={[1, 1.25]} // the key art is 1536 px wide: more pixels only cost
      camera={{ fov: 38.9, near: 0.05, far: 1500, position: CAM_POS.toArray() }}
      gl={{
        antialias: true,
        toneMapping: THREE.NoToneMapping,
        outputColorSpace: THREE.SRGBColorSpace,
        powerPreference: 'high-performance',
      }}
      onCreated={(state) => {
        if (import.meta.env.DEV) (window as unknown as { __r3f: unknown }).__r3f = state
      }}
    >
      <directionalLight color="#ffe6c4" intensity={2.45} position={[-3.5, 5, 6]} />
      <hemisphereLight color="#b4d4f4" groundColor="#ead2ae" intensity={1.0} />
      <pointLight color="#ffe0ae" intensity={2.2} distance={3.2} decay={1.6} position={[-0.25, 1.1, 0.35]} />
      <Suspense fallback={null}>
        <Sky />
        <World />
        <Alu />
        <Motes />
        <Ready />
      </Suspense>
      <CameraRig />
      <EffectComposer multisampling={2}>
        <Bloom luminanceThreshold={1.1} mipmapBlur intensity={0.45} radius={0.55} />
      </EffectComposer>
    </Canvas>
  )
}
