import { useState, useRef, useEffect } from 'react'
import { CARD_IMAGES, getCardImage } from '../utils/cardImages'

// Card sizes - matches PNG aspect ratio (300x527)
const sizes = {
  small: { width: 90, height: 158 },
  normal: { width: 140, height: 246 },
  large: { width: 180, height: 316 }
}

// Liquid glass transition with spring physics
const transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.5s ease, filter 0.3s ease'

// Slow reveal hover delay in ms
const SLOW_REVEAL_DELAY = 800

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

export default function Card3D({ card = null, isRevealed = false, onClick, size = 'normal', enableHover = false, hoverCard = null, enableSlowReveal = false }) {
  const [rot, setRot] = useState({ x: 0, y: 0 })
  const [hovered, setHovered] = useState(false)
  const [showShimmer, setShowShimmer] = useState(false)
  const [mousePos, setMousePos] = useState({ x: 0.5, y: 0.5 }) // Normalized 0-1
  const ref = useRef(null)
  const hoverTimerRef = useRef(null)

  const { width, height } = sizes[size]
  const displayCard = hovered && hoverCard ? hoverCard : card
  const showFace = (enableHover && hovered && hoverCard) || isRevealed

  // Handle slow reveal shimmer effect
  useEffect(() => {
    if (enableSlowReveal && hovered) {
      // Start shimmer after delay
      hoverTimerRef.current = setTimeout(() => {
        setShowShimmer(true)
      }, SLOW_REVEAL_DELAY)
    } else {
      setShowShimmer(false)
      if (hoverTimerRef.current) {
        clearTimeout(hoverTimerRef.current)
      }
    }

    return () => {
      if (hoverTimerRef.current) {
        clearTimeout(hoverTimerRef.current)
      }
    }
  }, [enableSlowReveal, hovered])

  const onMove = (e) => {
    if (!ref.current) return
    const r = ref.current.getBoundingClientRect()
    // Track rotation
    setRot({
      x: ((e.clientY - r.top - r.height/2) / (r.height/2)) * -12,
      y: ((e.clientX - r.left - r.width/2) / (r.width/2)) * 12
    })
    // Track normalized mouse position for glow effect
    setMousePos({
      x: (e.clientX - r.left) / r.width,
      y: (e.clientY - r.top) / r.height
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

  // Subtle iridescent glow that follows mouse position
  const glowX = mousePos.x * 100
  const glowY = mousePos.y * 100
  const glowOverlay = hovered ? {
    position: 'absolute',
    inset: -4,
    borderRadius: 16,
    background: `radial-gradient(
      circle at ${glowX}% ${glowY}%,
      rgba(139, 92, 246, 0.15) 0%,
      rgba(6, 182, 212, 0.08) 25%,
      rgba(236, 72, 153, 0.04) 50%,
      transparent 60%
    )`,
    filter: 'blur(12px)',
    opacity: 0.5,
    transition: 'background 0.2s ease-out',
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
          {/* Slow reveal shimmer effect */}
          {enableSlowReveal && (
            <div
              className={`selection-card-shimmer ${showShimmer ? 'active' : ''}`}
              style={{
                transition: 'opacity 0.6s ease',
                opacity: showShimmer ? 1 : (hovered ? 0.3 : 0),
              }}
            />
          )}
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
              transform: displayCard.reversed ? 'rotate(180deg)' : 'none',
              position: 'relative'
            }}>
              <img
                src={getCardImage(displayCard)}
                alt={displayCard.name}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  filter: displayCard.reversed ? 'brightness(0.92) saturate(0.9)' : 'none'
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
              {/* Reversed card shadow/vignette treatment */}
              {displayCard.reversed && (
                <>
                  <div className="reversed-card-overlay" />
                  <div className="reversed-card-vignette" />
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
