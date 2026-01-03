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
      <p className="text-slate-400 text-xs">{card.name.split(' ').slice(-2).join(' ')}</p>
      {card.reversed && <p className="text-amber-500/80 text-xs">Reversed</p>}
    </div>
  ) : (
    <div className="mt-2 md:mt-3">
      <p className="text-slate-300 text-xs md:text-sm font-medium max-w-[120px] md:max-w-none mx-auto">{card.name}</p>
      {card.reversed && <p className="text-amber-500/80 text-xs mt-1">Reversed</p>}
      {showKeywords && (
        <div className={`mt-2 max-w-[140px] mx-auto transition-opacity duration-300 ${hovered ? 'opacity-100' : 'opacity-0'}`}>
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
      {hovered && <PositionTooltip position={position} showName={variant !== 'celtic'} />}

      {variant === 'standard' && (
        <p className="text-slate-500 text-xs md:text-sm mb-2 md:mb-3 font-medium cursor-help">
          {position.name}
        </p>
      )}

      <Card3D
        card={card}
        isRevealed={isRevealed}
        onClick={() => !isRevealed && isDealt && onReveal()}
        size={size}
        enableHover={isRevealed}
      />

      {isRevealed && !hideInlineLabel && cardInfo}
    </div>
  )
}
