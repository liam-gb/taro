import { useState, useRef } from 'react'
import { CARD_IMAGES, getCardImage } from '../utils/cardImages'

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

  // Responsive card sizes
  const sizes = {
    small: { width: 90, height: 148 },
    normal: { width: 140, height: 230 },
    large: { width: 180, height: 295 }
  }

  const s = sizes[size]

  const handleMouseMove = (e) => {
    if (!cardRef.current) return
    const rect = cardRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    setRotation({
      x: ((y - centerY) / centerY) * -10,
      y: ((x - centerX) / centerX) * 10
    })
  }

  const handleMouseLeave = () => {
    setRotation({ x: 0, y: 0 })
    setIsHovered(false)
  }

  const displayCard = isHovered && hoverCard ? hoverCard : card
  const showFace = (enableHover && isHovered && hoverCard) || isRevealed

  return (
    <div
      ref={cardRef}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      className="cursor-pointer"
      style={{ width: s.width, height: s.height, perspective: 1000 }}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'relative',
          transformStyle: 'preserve-3d',
          transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
          transform: `
            rotateX(${rotation.x}deg)
            rotateY(${rotation.y}deg)
            ${isHovered ? 'translateZ(12px) scale(1.03)' : ''}
          `,
        }}
      >
        {/* Card Back */}
        <div
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            backfaceVisibility: 'hidden',
            borderRadius: 8,
            overflow: 'hidden',
            boxShadow: isHovered
              ? '0 25px 50px rgba(0,0,0,0.5), 0 0 30px rgba(147, 112, 219, 0.2)'
              : '0 10px 30px rgba(0,0,0,0.4)',
            transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: showFace ? 'rotateY(180deg)' : 'rotateY(0deg)',
          }}
        >
          <img
            src={CARD_IMAGES.back}
            alt="Card back"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        {/* Card Face */}
        <div
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            backfaceVisibility: 'hidden',
            borderRadius: 8,
            overflow: 'hidden',
            boxShadow: isHovered ? '0 25px 50px rgba(0,0,0,0.5)' : '0 10px 30px rgba(0,0,0,0.4)',
            transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: showFace ? 'rotateY(0deg)' : 'rotateY(-180deg)',
          }}
        >
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
