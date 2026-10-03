import { useEffect, useRef, useState } from 'react'
import Scene from './Scene'
import Bubble from './Bubble'
import { pointer, useHero } from './store'
import s from './Hero.module.css'

/**
 * The Arrival screen (DESIGN section 8): the 3D coast underneath, and the only chrome
 * allowed on top: wordmark, the controls pill, Alu's bubble (in the scene), and the
 * "SCROLL TO FOLLOW" label. The sun glare is DOM so it stays crisp and cheap.
 */
export default function Hero() {
  const ready = useHero((st) => st.ready)
  const glare = useRef<HTMLDivElement>(null)
  const [night, setNight] = useState(false)
  const [sound, setSound] = useState(false)

  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      pointer.x = (e.clientX / window.innerWidth) * 2 - 1
      pointer.y = -((e.clientY / window.innerHeight) * 2 - 1)
      pointer.active = true
      pointer.idle = 0
      if (glare.current) {
        glare.current.style.transform = `translate3d(${pointer.x * -18}px, ${pointer.y * 14}px, 0)`
      }
    }
    const onLeave = () => {
      pointer.x = 0
      pointer.y = 0
    }
    window.addEventListener('pointermove', onMove, { passive: true })
    document.documentElement.addEventListener('mouseleave', onLeave)
    return () => {
      window.removeEventListener('pointermove', onMove)
      document.documentElement.removeEventListener('mouseleave', onLeave)
    }
  }, [])

  useEffect(() => {
    document.documentElement.dataset.theme = night ? 'night' : 'day'
  }, [night])

  return (
    <div className={s.hero}>
      <div className={s.canvas}>
        <Scene />
      </div>
      <div ref={glare} className={s.glare} aria-hidden="true" />
      <Bubble />

      <header className={s.chrome}>
        <a className={s.wordmark} href="/" aria-label="Ashish Gupta, home">
          <img src="/images/logo-ocean.svg" alt="" width="38" height="38" />
          <span>Ashish Gupta</span>
        </a>
        <div className={`${s.controls} ${night ? s.controlsNight : ''}`}>
          <button
            type="button"
            className={s.iconBtn}
            aria-pressed={sound}
            aria-label={sound ? 'Sound on' : 'Sound off'}
            onClick={() => setSound((v) => !v)}
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 9.5h3.2L12 5.5v13l-4.8-4H4z" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
              {sound && (
                <path d="M15.5 9.2a4 4 0 0 1 0 5.6M18.2 6.8a7.4 7.4 0 0 1 0 10.4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
              )}
            </svg>
          </button>
          <button
            type="button"
            className={s.iconBtn}
            aria-pressed={night}
            aria-label={night ? 'Switch to day' : 'Switch to night'}
            onClick={() => setNight((v) => !v)}
          >
            {night ? (
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M19.5 14.6A7.8 7.8 0 0 1 9.4 4.5a7.8 7.8 0 1 0 10.1 10.1z" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" strokeWidth="1.8" />
                <path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
              </svg>
            )}
          </button>
          <span className={s.divider} />
          <button type="button" className={s.menuBtn} aria-haspopup="dialog">
            <svg viewBox="0 0 16 10" aria-hidden="true">
              <path d="M1 1.5h14M1 8.5h9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
            </svg>
            Menu
          </button>
        </div>
      </header>

      <div className={s.scrollHint} aria-hidden="true">
        SCROLL TO FOLLOW
      </div>

      <div className={`${s.veil} ${ready ? s.veilGone : ''}`} aria-hidden={ready}>
        <img src="/images/logo-ocean.svg" alt="" width="44" height="44" />
      </div>
    </div>
  )
}
