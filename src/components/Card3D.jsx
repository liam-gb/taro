import { useState, useRef } from 'react'
import { CARD_IMAGES, getCardImage } from '../utils/cardImages'

// Card sizes - matches PNG aspect ratio (300x527)
const sizes = {
  small: { width: 90, height: 158 },
  normal: { width: 140, height: 246 },
  large: { width: 180, height: 316 }
}

const transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s ease'
const shadow = {
  idle: '0 10px 30px rgba(0,0,0,0.4)',
  hover: '0 25px 50px rgba(0,0,0,0.5)',
  revealed: '0 15px 40px rgba(0,0,0,0.4), 0 0 20px rgba(147,112,219,0.15)'
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
    setRot({ x: ((e.clientY - r.top - r.height/2) / (r.height/2)) * -10, y: ((e.clientX - r.left - r.width/2) / (r.width/2)) * 10 })
  }

  const face = { position: 'absolute', width: '100%', height: '100%', backfaceVisibility: 'hidden', borderRadius: 8, overflow: 'hidden', transition }

  return (
    <div ref={ref} onClick={onClick} onMouseMove={onMove} onMouseEnter={() => setHovered(true)} onMouseLeave={() => { setRot({ x: 0, y: 0 }); setHovered(false) }}
      className="cursor-pointer" style={{ width, height, perspective: 1000 }}>
      <div style={{ width: '100%', height: '100%', position: 'relative', transformStyle: 'preserve-3d', transition,
        transform: `rotateX(${rot.x}deg) rotateY(${rot.y}deg) ${hovered ? 'translateZ(12px) scale(1.03)' : ''}` }}>
        <div style={{ ...face, boxShadow: hovered ? `${shadow.hover}, 0 0 30px rgba(147,112,219,0.2)` : shadow.idle, transform: showFace ? 'rotateY(180deg)' : 'rotateY(0deg)' }}>
          <img src={CARD_IMAGES.back} alt="Card back" style={{ width: '100%', height: '100%', objectFit: 'cover' }} draggable={false} />
        </div>
        <div style={{ ...face, boxShadow: hovered ? shadow.hover : (isRevealed ? shadow.revealed : shadow.idle), transform: showFace ? 'rotateY(0deg)' : 'rotateY(-180deg)' }}>
          {displayCard && (
            <div style={{ width: '100%', height: '100%', transform: displayCard.reversed ? 'rotate(180deg)' : 'none' }}>
              <img src={getCardImage(displayCard)} alt={displayCard.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} draggable={false} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
