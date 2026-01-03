import { useState, useRef } from 'react'
import { CARD_IMAGES, getCardImage } from '../utils/cardImages'

// Card sizes - matches PNG aspect ratio (300x527)
const sizes = {
  small: { width: 90, height: 158 },
  normal: { width: 140, height: 246 },
  large: { width: 180, height: 316 }
}

// Liquid glass transition with spring physics
const transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.5s ease, filter 0.3s ease'

// Mystical shadow system with iridescent glow
const shadow = {
  idle: `
    0 20px 40px -10px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.1)
  `,
  hover: `
    0 30px 60px -15px rgba(0, 0, 0, 0.6),
    0 0 50px rgba(139, 92, 246, 0.25),
    0 0 100px rgba(6, 182, 212, 0.1),
    0 0 0 1px rgba(139, 92, 246, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.15)
  `,
  revealed: `
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 40px rgba(139, 92, 246, 0.2),
    0 0 80px rgba(236, 72, 153, 0.1),
    0 0 0 1px rgba(139, 92, 246, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.1)
  `
}

export default function Card3D({ card = null, isRevealed = false, onClick, size = 'normal', enableHover = false, hoverCard = null }) {
  const [rot, setRot] = useState({ x: 0, y: 0 })
  const [hovered, setHovered] = useState(false)
  const ref = useRef(null)

  const { width, height } = sizes[size]
  const displayCard = hovered && hoverCard ? hoverCard : card
  const showFace = (enableHover && hovered && hoverCard) || isRevealed

  const onMove = (e) => {
    if (!ref.current) return
    const r = ref.current.getBoundingClientRect()
    setRot({
      x: ((e.clientY - r.top - r.height/2) / (r.height/2)) * -12,
      y: ((e.clientX - r.left - r.width/2) / (r.width/2)) * 12
    })
  }

  const face = {
    position: 'absolute',
    width: '100%',
    height: '100%',
    backfaceVisibility: 'hidden',
    borderRadius: 12,
    overflow: 'hidden',
    transition
  }

  // Iridescent gradient overlay for the card edge
  const glowOverlay = hovered ? {
    position: 'absolute',
    inset: -2,
    borderRadius: 14,
    background: `linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.4) 0%,
      rgba(6, 182, 212, 0.3) 25%,
      rgba(236, 72, 153, 0.3) 50%,
      rgba(245, 158, 11, 0.2) 75%,
      rgba(139, 92, 246, 0.4) 100%
    )`,
    filter: 'blur(8px)',
    opacity: 0.6,
    animation: 'iridescent-shift 4s ease infinite',
    zIndex: -1,
    pointerEvents: 'none'
  } : null

  return (
    <div
      ref={ref}
      onClick={onClick}
      onMouseMove={onMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => { setRot({ x: 0, y: 0 }); setHovered(false) }}
      className="cursor-pointer relative"
      style={{ width, height, perspective: 1200 }}
    >
      {/* Iridescent glow effect on hover */}
      {glowOverlay && <div style={glowOverlay} />}

      <div style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        transformStyle: 'preserve-3d',
        transition,
        transform: `rotateX(${rot.x}deg) rotateY(${rot.y}deg) ${hovered ? 'translateZ(20px) scale(1.05)' : ''}`
      }}>
        {/* Card Back */}
        <div style={{
          ...face,
          boxShadow: hovered ? shadow.hover : shadow.idle,
          transform: showFace ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}>
          <img
            src={CARD_IMAGES.back}
            alt="Card back"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
            draggable={false}
          />
          {/* Subtle glass reflection overlay */}
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.05) 100%)',
            pointerEvents: 'none'
          }} />
        </div>

        {/* Card Front */}
        <div style={{
          ...face,
          boxShadow: hovered ? shadow.hover : (isRevealed ? shadow.revealed : shadow.idle),
          transform: showFace ? 'rotateY(0deg)' : 'rotateY(-180deg)',
        }}>
          {displayCard && (
            <div style={{
              width: '100%',
              height: '100%',
              transform: displayCard.reversed ? 'rotate(180deg)' : 'none'
            }}>
              <img
                src={getCardImage(displayCard)}
                alt={displayCard.name}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
                draggable={false}
              />
              {/* Subtle glass reflection overlay on front */}
              <div style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 40%, rgba(255,255,255,0.03) 100%)',
                pointerEvents: 'none'
              }} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
