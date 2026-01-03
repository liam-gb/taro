import { useState } from 'react'
import Card3D from './Card3D'
import PositionTooltip from './PositionTooltip'
import KeywordList from './KeywordList'

export default function CardSlot({
  card,
  position,
  isDealt,
  isRevealed,
  onReveal,
  size = 'normal',
  variant = 'standard',
  showKeywords = false,
  isMobile = false,
  hideInlineLabel = false
}) {
  const [hovered, setHovered] = useState(false)

  const cardInfo = variant === 'celtic' ? (
    <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
      <p className="text-slate-300/90 text-xs font-light tracking-wide">
        {card.name.split(' ').slice(-2).join(' ')}
      </p>
      {card.reversed && (
        <p className="text-amber-400/80 text-xs font-medium mt-0.5">Reversed</p>
      )}
    </div>
  ) : (
    <div className="mt-3 md:mt-4">
      <p className="text-slate-200/90 text-xs md:text-sm font-light tracking-wide max-w-[120px] md:max-w-none mx-auto">
        {card.name}
      </p>
      {card.reversed && (
        <p className="text-amber-400/80 text-xs font-medium mt-1.5 tracking-wide">
          Reversed
        </p>
      )}
      {showKeywords && (
        <div className={`mt-3 max-w-[140px] mx-auto transition-all duration-500 ${
          hovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
        }`}>
          <KeywordList keywords={card.keywords} variant="badges" limit={3} />
        </div>
      )}
    </div>
  )

  return (
    <div
      className="relative group"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Tooltip */}
      {hovered && (
        <PositionTooltip
          position={position}
          showName={true}
        />
      )}


      {/* The Card */}
      <Card3D
        card={card}
        isRevealed={isRevealed}
        onClick={() => !isRevealed && isDealt && onReveal()}
        size={size}
        enableHover={isRevealed}
      />

      {/* Card info (name, reversed status, keywords) */}
      {isRevealed && !hideInlineLabel && cardInfo}
    </div>
  )
}
