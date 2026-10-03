import * as THREE from 'three'
import { BACKDROP, CX, F_PX, HORIZON_Y } from './heroCam'

/**
 * Shader pieces for the hero. The near world is painted by projecting the key-art plate from
 * the rest camera (so at rest the screen is the key art and moving the camera gives true
 * parallax); the far world is the backdrop on a dome at infinity. Grass and pines still move:
 * the projection reads the rest position, so the paint sticks to a swaying blade.
 */

export type SwayUniforms = {
  uTime: { value: number }
  uCursor: { value: THREE.Vector3 } // world-space pointer hit on the ground
  uPush: { value: number } // how much the cursor bends blades (0 for trees)
  uAmp: { value: number } // wind amplitude in metres at full height
  uHeight: { value: number } // height at which a vertex has full weight
}

export function makeSwayUniforms(push: number, amp: number, height: number): SwayUniforms {
  return {
    uTime: { value: 0 },
    uCursor: { value: new THREE.Vector3(0, 0, 100) },
    uPush: { value: push },
    uAmp: { value: amp },
    uHeight: { value: height },
  }
}

const SWAY_DECL = `uniform float uTime; uniform vec3 uCursor; uniform float uPush; uniform float uAmp; uniform float uHeight;`
const SWAY_BODY = `
  {
    float w = clamp(position.y / uHeight, 0.0, 1.0);
    w = w * w;
    vec3 base = modelMatrix[3].xyz;
    float gust = sin(uTime * 1.35 + base.x * 0.55 + base.z * 0.4) * 0.7 + sin(uTime * 2.9 + base.z * 1.3) * 0.3;
    vec3 disp = vec3(gust * uAmp, 0.0, sin(uTime * 1.1 + base.x * 0.8) * uAmp * 0.35);
    vec2 d = base.xz - uCursor.xz;
    float dist = length(d);
    float push = smoothstep(0.9, 0.0, dist) * uPush;
    disp.xz += (dist > 1e-4 ? d / dist : vec2(0.0)) * push;
    disp.y -= push * 0.3;
    // world-space displacement back into local space (uniform scale, rotation only)
    transformed += transpose(mat3(modelMatrix)) * disp * w;
  }`

/** Bend vertices by height: wind (two sines) plus a radial push away from the cursor. */
export function injectSway(material: THREE.Material, u: SwayUniforms) {
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, u)
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>\n${SWAY_DECL}`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>\n${SWAY_BODY}`)
  }
  material.customProgramCacheKey = () => 'sway'
}

export type ProjUniforms = {
  uPlate: { value: THREE.Texture | null }
  uProjVP: { value: THREE.Matrix4 }
}

/**
 * Turns an unlit vertex-colour material into a projected one: the colour is the plate seen
 * through the rest camera at the vertex's rest position. Off the plate it falls back to the
 * vertex colour (the plate sampled per vertex in Blender, from where the camera sees).
 * With `sway`, vertices also move like the pines while keeping their paint.
 */
export function injectProjection(material: THREE.MeshBasicMaterial, u: ProjUniforms, sway?: SwayUniforms) {
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, u, sway ?? {})
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform mat4 uProjVP;
        varying vec4 vProj;
        ${sway ? SWAY_DECL : ''}`,
      )
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        vProj = uProjVP * modelMatrix * vec4(position, 1.0);
        ${sway ? SWAY_BODY : ''}`,
      )
    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform sampler2D uPlate;
        varying vec4 vProj;`,
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        {
          vec2 uv = vProj.xy / vProj.w * 0.5 + 0.5;
          vec2 inside = step(vec2(0.0), uv) * step(uv, vec2(1.0));
          float ok = inside.x * inside.y * step(0.0, vProj.w);
          vec3 plate = texture2D(uPlate, clamp(uv, 0.0, 1.0)).rgb;
          diffuseColor.rgb = mix(diffuseColor.rgb, plate, ok);
        }`,
      )
  }
  material.customProgramCacheKey = () => (sway ? 'proj-sway' : 'proj')
}

/**
 * The backdrop: a dome at infinity that shows the matte painting by view direction, mapped
 * exactly as the rest camera saw the key art. Directions past the painted area clamp to its
 * edge (sky above, sea below). The sea gets a slow glint shimmer.
 */
export function backdropMaterial(map: THREE.Texture) {
  return new THREE.ShaderMaterial({
    side: THREE.BackSide,
    depthWrite: false,
    fog: false,
    toneMapped: false,
    uniforms: {
      uMap: { value: map },
      uTime: { value: 0 },
      uF: { value: F_PX },
      uCenter: { value: new THREE.Vector2(CX + BACKDROP.padX, HORIZON_Y + BACKDROP.padTop) },
      uSize: { value: new THREE.Vector2(BACKDROP.w, BACKDROP.h) },
    },
    vertexShader: `
      varying vec3 vWorld;
      void main() {
        vec4 wp = modelMatrix * vec4(position, 1.0);
        vWorld = wp.xyz;
        gl_Position = projectionMatrix * viewMatrix * wp;
      }`,
    fragmentShader: `
      uniform sampler2D uMap; uniform float uTime; uniform float uF;
      uniform vec2 uCenter; uniform vec2 uSize;
      varying vec3 vWorld;
      float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      void main() {
        vec3 d = normalize(vWorld - cameraPosition);
        float fwd = max(-d.z, 1e-3);
        vec2 px = vec2(uCenter.x + uF * d.x / fwd, uCenter.y - uF * d.y / fwd);
        vec2 uv = vec2(px.x / uSize.x, 1.0 - px.y / uSize.y);
        vec3 c = texture2D(uMap, clamp(uv, vec2(0.0005), vec2(0.9995))).rgb;
        // sea glints: sparse cells that twinkle, denser toward the horizon line
        float below = px.y - uCenter.y;
        if (below > 2.0) {
          vec2 cell = floor(vec2(px.x / 7.0, below / 2.5));
          float h = hash(cell);
          float tw = sin(uTime * (1.2 + h * 2.0) + h * 40.0) * 0.5 + 0.5;
          float g = smoothstep(0.993, 1.0, h) * pow(tw, 8.0) * smoothstep(140.0, 10.0, below);
          c += vec3(0.9, 1.0, 1.0) * g * 0.12;
        }
        gl_FragColor = vec4(c, 1.0);
        #include <colorspace_fragment>
      }`,
  })
}

/**
 * The gate's glass: almost clear over the sky, a warm milky glow that thickens toward the
 * sill (as painted), a soft brightening at the inner edges and two faint diagonal streaks.
 * uGlow lifts it when the pointer comes near.
 */
export function glassMaterial() {
  return new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide,
    toneMapped: false,
    uniforms: {
      uTime: { value: 0 },
      uGlow: { value: 0 },
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `
      uniform float uTime; uniform float uGlow;
      varying vec2 vUv;
      void main() {
        vec2 uv = vec2(vUv.x, 1.0 - vUv.y); // glTF flips V; this puts 0 back at the sill
        float low = 1.0 - smoothstep(0.0, 0.34, uv.y);
        float a = 0.62 * pow(low, 1.25);
        // as painted: the right inner edge glows, the left and top only a little
        float edge = smoothstep(0.05, 0.0, uv.x) * 0.07 + smoothstep(0.08, 0.0, 1.0 - uv.x) * 0.2
                   + smoothstep(0.04, 0.0, 1.0 - uv.y) * 0.06;
        float diag = uv.x * 0.62 + uv.y;
        float streak = smoothstep(0.035, 0.0, abs(fract(diag * 0.9 + 0.12) - 0.5) - 0.012) * 0.05
                     + smoothstep(0.02, 0.0, abs(fract(diag * 0.9 + 0.33) - 0.5) - 0.006) * 0.035;
        float breath = 0.92 + 0.08 * sin(uTime * 0.8);
        a = (a + edge + streak) * breath * (1.0 + uGlow * 0.35);
        vec3 col = mix(vec3(1.0, 0.975, 0.93), vec3(1.0, 0.9, 0.7), low);
        // a touch over 1 at the sill so the bloom pass picks it up
        col *= 1.0 + low * low * (0.35 + uGlow * 0.4);
        gl_FragColor = vec4(col, clamp(a, 0.0, 0.9));
        #include <colorspace_fragment>
      }`,
  })
}
