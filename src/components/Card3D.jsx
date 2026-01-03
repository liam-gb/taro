import { useState, useRef } from 'react'
import { CARD_IMAGES, getCardImage } from '../utils/cardImages'
import { CARD_SIZES, CARD_TRANSITION, CARD_SHADOWS, HOVER_ROTATION_SCALE } from '../constants'

export default function Card3D({
  card = null,
  isRevealed = false,
  onClick,
  size = 'normal',
  enableHover = false,
  hoverCard = null
}) {
  const [rotation, setRotation] = useState({ x: 0, y: 0 })
  const [isHovered, setIsHovered] = useState(false)
  const cardRef = useRef(null)

  const { width, height } = CARD_SIZES[size]

  const handleMouseMove = (e) => {
    if (!cardRef.current) return
    const rect = cardRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    setRotation({
      x: ((y - centerY) / centerY) * -HOVER_ROTATION_SCALE,
      y: ((x - centerX) / centerX) * HOVER_ROTATION_SCALE
    })
  }

  const handleMouseLeave = () => {
    setRotation({ x: 0, y: 0 })
    setIsHovered(false)
  }

  const displayCard = isHovered && hoverCard ? hoverCard : card
  const showFace = (enableHover && isHovered && hoverCard) || isRevealed
  const shadow = isHovered ? CARD_SHADOWS.hoveredGlow : CARD_SHADOWS.idle
  const shadowSimple = isHovered ? CARD_SHADOWS.hovered : CARD_SHADOWS.idle

  const cardFaceStyle = {
    position: 'absolute',
    width: '100%',
    height: '100%',
    backfaceVisibility: 'hidden',
    borderRadius: 8,
    overflow: 'hidden',
    transition: CARD_TRANSITION
  }

  return (
    <div
      ref={cardRef}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      className="cursor-pointer"
      style={{ width, height, perspective: 1000 }}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'relative',
          transformStyle: 'preserve-3d',
          transition: CARD_TRANSITION,
          transform: `
            rotateX(${rotation.x}deg)
            rotateY(${rotation.y}deg)
            ${isHovered ? 'translateZ(12px) scale(1.03)' : ''}
          `,
        }}
      >
        {/* Card Back */}
        <div style={{ ...cardFaceStyle, boxShadow: shadow, transform: showFace ? 'rotateY(180deg)' : 'rotateY(0deg)' }}>
          <img
            src={CARD_IMAGES.back}
            alt="Card back"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        {/* Card Face */}
        <div style={{ ...cardFaceStyle, boxShadow: shadowSimple, transform: showFace ? 'rotateY(0deg)' : 'rotateY(-180deg)' }}>
          {displayCard && (
            <div style={{
              width: '100%',
              height: '100%',
              transform: displayCard.reversed ? 'rotate(180deg)' : 'none',
            }}>
              <img
                src={getCardImage(displayCard)}
                alt={displayCard.name}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
