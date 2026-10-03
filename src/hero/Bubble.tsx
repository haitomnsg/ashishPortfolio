import { useHero, bubbleAnchor } from './store'
import s from './Hero.module.css'

/**
 * Alu's speech bubble: plain DOM, placed over the canvas. Alu's frame loop projects his
 * head into screen space and writes the position straight onto this element, so there
 * is no portal and no React work per frame. Styled per docs/design/ui-v2.html.
 */
export default function Bubble() {
  const open = useHero((st) => st.bubble)
  const line = useHero((st) => st.line)
  const [before, after] = line.text.split(line.word)
  return (
    <div
      ref={(el) => {
        bubbleAnchor.el = el
      }}
      className={s.anchor}
      aria-hidden={!open}
    >
      <div
        ref={(el) => {
          if (!el) return
          const measure = () => (bubbleAnchor.width = el.offsetWidth)
          measure()
          new ResizeObserver(measure).observe(el)
        }}
        className={`${s.bubble} ${open ? s.bubbleOpen : ''}`}
        role="status"
        aria-live="polite"
      >
        <div className={s.card}>
          <div className={s.bubbleHead}>
            <svg className={s.badge} viewBox="0 0 30 22" aria-hidden="true">
              <rect width="30" height="22" rx="7" fill="#03045E" />
              <ellipse cx="10.4" cy="9.8" rx="3.4" ry="4.4" fill="#7FE6FF" />
              <ellipse cx="19.6" cy="9.8" rx="3.4" ry="4.4" fill="#7FE6FF" />
              <path d="M13.2 16.1q1.8 1.5 3.6 0" fill="none" stroke="#7FE6FF" strokeWidth="1.3" strokeLinecap="round" />
            </svg>
            <span className={s.name}>ALU</span>
          </div>
          <div className={s.line}>
            {before}
            <em>{line.word}</em>
            {after}
          </div>
        </div>
        <svg className={s.tail} viewBox="0 0 34 24" aria-hidden="true">
          <path d="M0 0H28C27 9 29 17 34 24C21 21 9 13 0 0Z" />
        </svg>
      </div>
    </div>
  )
}
