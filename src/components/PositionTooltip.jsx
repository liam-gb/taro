export default function PositionTooltip({ position, showName = true, card = null }) {
  const hasCard = card !== null
  const topOffset = hasCard ? '-top-20' : (showName ? '-top-16' : '-top-12')
  const descColor = showName ? 'text-slate-500' : 'text-slate-400'

  return (
    <div className={`absolute ${topOffset} left-1/2 -translate-x-1/2 bg-slate-800 px-3 py-2 rounded-lg text-xs whitespace-nowrap z-20 border border-slate-700`}>
      {showName && <div className="text-violet-400 font-medium">{position.name}</div>}
      <div className={descColor}>{position.description}</div>
      {hasCard && (
        <div className="text-slate-300 mt-1 font-medium">
          {card.name}{card.reversed && <span className="text-amber-500/80 ml-1">(R)</span>}
        </div>
      )}
    </div>
  )
}
