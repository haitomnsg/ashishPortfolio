import * as THREE from 'three'

/**
 * The key art's camera (inspo/Section_One.png, 1536 x 1024), shared by everything that has
 * to line up with it. Mirrors Hero_Cam in docs/world/hero_build.py and the constants in
 * docs/world/backdrop_build.py: a 34 mm lens on a 36 mm sensor, level, with the lens shifted
 * so the sea horizon sits on row 620. Blender (x, y, z) is three.js (x, z, -y).
 */
export const IMG_W = 1536
export const IMG_H = 1024
export const F_PX = (34 / 36) * IMG_W // focal length in key-art pixels
export const CX = IMG_W / 2
export const HORIZON_Y = 620

/** Vertical extent of the key art as tangents of the view angle (up positive). */
export const TAN_TOP = HORIZON_Y / F_PX
export const TAN_BOTTOM = -(IMG_H - HORIZON_Y) / F_PX
export const TAN_HALF_W = CX / F_PX

/** The rest pose: the hero camera exactly as the key art was "shot". */
export const CAM_POS = new THREE.Vector3(0, 0.8384, 7.17)

/** Backdrop texture layout (public/images/hero/backdrop.webp): the key art plus padding. */
export const BACKDROP = { url: '/images/hero/backdrop.webp', padX: 160, padTop: 288, w: 1856, h: 1376 }
export const PLATE_URL = '/images/hero/plate.webp'

/** The part of the key art that must stay on screen when the view narrows: Alu to the gate. */
export const FOCUS_LEFT = (440 - CX) / F_PX
export const FOCUS_RIGHT = (906 - CX) / F_PX

/**
 * Sets a perspective camera to look through the tangent window [left, right] x [bottom, top]
 * (an off-axis frustum, i.e. a lens shift).
 */
export function setLensWindow(cam: THREE.PerspectiveCamera, left: number, right: number, bottom: number, top: number) {
  const half = (top - bottom) / 2
  const halfW = (right - left) / 2
  const fov = THREE.MathUtils.radToDeg(2 * Math.atan(half))
  const aspect = halfW / half
  if (Math.abs(cam.fov - fov) > 1e-6 || Math.abs(cam.aspect - aspect) > 1e-6) {
    cam.fov = fov
    cam.aspect = aspect
  }
  cam.updateProjectionMatrix()
  cam.projectionMatrix.elements[8] = (right + left) / 2 / halfW
  cam.projectionMatrix.elements[9] = (top + bottom) / 2 / half
  cam.projectionMatrixInverse.copy(cam.projectionMatrix).invert()
}

/** View-projection matrix of the rest camera: what the plate was "painted" through. */
export function restViewProjection(): THREE.Matrix4 {
  const cam = new THREE.PerspectiveCamera(40, IMG_W / IMG_H, 0.05, 2000)
  cam.position.copy(CAM_POS)
  cam.lookAt(CAM_POS.x, CAM_POS.y, CAM_POS.z - 1)
  cam.updateMatrixWorld()
  setLensWindow(cam, -TAN_HALF_W, TAN_HALF_W, TAN_BOTTOM, TAN_TOP)
  return new THREE.Matrix4().multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse)
}
