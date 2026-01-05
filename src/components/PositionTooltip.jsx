export default function PositionTooltip({ position, card, showName = true }) {
  const hasCard = card && card.name
  const topOffset = hasCard ? '-top-24' : (showName ? '-top-20' : '-top-16')

  return (
    <div className={`absolute ${topOffset} left-1/2 tooltip-glass px-4 py-3 rounded-xl text-xs whitespace-nowrap z-[200]`}
      style={{ transform: 'translateX(-50%)', animation: 'tooltip-fade-in 0.2s ease' }}>
      {/* Decorative top accent */}
      <div className="absolute -top-px left-4 right-4 h-px bg-gradient-to-r from-transparent via-amber-500/50 to-transparent" />

      {hasCard && (
        <div className="text-slate-200/90 font-medium tracking-wide mb-1.5">
          {card.name}
          {card.reversed && <span className="text-amber-400/80 ml-1.5 text-[10px]">(R)</span>}
        </div>
      )}
      {showName && (
        <div className="text-amber-400/90 font-medium tracking-wide mb-1">{position.name}</div>
      )}
      <div className="text-slate-400/90 font-light">{position.description}</div>

      {/* Arrow pointer */}
      <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-[rgba(15,15,25,0.9)] border-r border-b border-white/10" />
    </div>
  )
}
