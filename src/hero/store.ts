import { create } from 'zustand'

/**
 * Shared, mutable state for the hero. Pointer values are written every frame, so they
 * live on a plain object (no React re-renders); UI flags go through zustand setters.
 */
export const pointer = {
  /** normalised device coords, -1..1, updated on pointermove; (0,0) when idle */
  x: 0,
  y: 0,
  /** smoothed copy, driven by the scene's frame loop */
  sx: 0,
  sy: 0,
  /** where the pointer ray hits the ground plane (world space, three.js Y-up) */
  gx: 0,
  gz: 6,
  /** true once the pointer has moved at least once */
  active: false,
  /** seconds since the pointer last moved */
  idle: 0,
}

/** The sky cube map for reflective materials (written by Sky.tsx, read by World.tsx). */
export const env: { map: import('three').Texture | null; version: number } = { map: null, version: 0 }

/** The DOM element the scene positions over Alu's head (see Bubble.tsx and Alu.tsx). */
export const bubbleAnchor: { el: HTMLDivElement | null } = { el: null }

type HeroState = {
  ready: boolean
  aluHover: boolean
  gateHover: boolean
  bubble: boolean
  line: { text: string; word: string }
  reducedMotion: boolean
  setReady: (v: boolean) => void
  setAluHover: (v: boolean) => void
  setGateHover: (v: boolean) => void
  setBubble: (v: boolean) => void
  say: (text: string, word: string) => void
}

export const useHero = create<HeroState>((set) => ({
  ready: false,
  aluHover: false,
  gateHover: false,
  bubble: false,
  line: { text: "I wasn't the first thing he built.", word: 'built' },
  reducedMotion:
    typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)').matches,
  setReady: (ready) => set({ ready }),
  setAluHover: (aluHover) => set({ aluHover }),
  setGateHover: (gateHover) => set({ gateHover }),
  setBubble: (bubble) => set({ bubble }),
  say: (text, word) => set({ line: { text, word }, bubble: true }),
}))
