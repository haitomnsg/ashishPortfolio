import * as THREE from 'three'

/**
 * Small vertex-shader injections for the stock three.js materials, so the world keeps
 * its lighting and vertex colours and still moves: wind on grass and pines, a cursor
 * push on grass, and a facet shimmer on the sea.
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

/** Bend vertices by height: wind (two sines) plus a radial push away from the cursor. */
export function injectSway(material: THREE.Material, u: SwayUniforms) {
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, u)
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uTime; uniform vec3 uCursor; uniform float uPush; uniform float uAmp; uniform float uHeight;`,
      )
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        {
          float w = clamp(position.y / uHeight, 0.0, 1.0);
          w = w * w;
          vec3 wp = (modelMatrix * vec4(position, 1.0)).xyz;
          vec3 base = modelMatrix[3].xyz;
          float gust = sin(uTime * 1.35 + base.x * 0.55 + base.z * 0.4) * 0.7 + sin(uTime * 2.9 + base.z * 1.3) * 0.3;
          vec3 disp = vec3(gust * uAmp, 0.0, sin(uTime * 1.1 + base.x * 0.8) * uAmp * 0.35);
          vec2 d = base.xz - uCursor.xz;
          float dist = length(d);
          float push = smoothstep(1.6, 0.0, dist) * uPush;
          disp.xz += (dist > 1e-4 ? d / dist : vec2(0.0)) * push;
          disp.y -= push * 0.35;
          // world-space displacement back into local space (uniform scale, rotation only)
          transformed += transpose(mat3(modelMatrix)) * disp * w;
        }`,
      )
  }
  material.customProgramCacheKey = () => 'sway'
}

export type SeaUniforms = { uTime: { value: number } }

/** Low, slow facet waves on the coarse sea grid. flatShading turns them into shimmer. */
export function injectSea(material: THREE.Material, u: SeaUniforms) {
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, u)
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\n uniform float uTime;')
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        {
          float a = sin(position.x * 0.35 + uTime * 0.9) * 0.22 + sin(position.z * 0.5 - uTime * 0.7) * 0.18
                  + sin((position.x + position.z) * 0.21 + uTime * 0.45) * 0.3;
          transformed.y += a;
        }`,
      )
  }
  material.customProgramCacheKey = () => 'sea'
}

/** Sky gradient: deep blue up, pale at the horizon. Also used for the glass env map. */
export const skyMaterial = () =>
  new THREE.ShaderMaterial({
    side: THREE.BackSide,
    depthWrite: false,
    fog: false,
    uniforms: {
      uTop: { value: new THREE.Color('#3FA2DE') },
      uHorizon: { value: new THREE.Color('#CFEAF7') },
      uSun: { value: new THREE.Vector3(-0.55, 0.62, 0.55).normalize() },
    },
    vertexShader: `
      varying vec3 vDir;
      void main() {
        vDir = normalize(position);
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform vec3 uTop; uniform vec3 uHorizon; uniform vec3 uSun;
      varying vec3 vDir;
      void main() {
        float h = clamp(vDir.y, -0.1, 1.0);
        float t = pow(smoothstep(-0.04, 0.48, h), 0.8);
        vec3 c = mix(uHorizon, uTop, t);
        float s = max(dot(normalize(vDir), uSun), 0.0);
        c += vec3(1.0, 0.95, 0.82) * (pow(s, 60.0) * 0.5 + pow(s, 6.0) * 0.12);
        gl_FragColor = vec4(c, 1.0);
        #include <colorspace_fragment>
      }`,
  })
